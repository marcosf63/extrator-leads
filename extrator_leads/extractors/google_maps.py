"""Extractor para Google Maps."""

import re
from typing import List, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from extrator_leads.extractors.base import BaseExtractor
from extrator_leads.core.models import Lead


class GoogleMapsExtractor(BaseExtractor):
    """Extractor de leads do Google Maps."""

    @property
    def fonte(self) -> str:
        """Retorna o nome da fonte."""
        return "google_maps"

    @classmethod
    def pode_extrair(cls, url: str) -> bool:
        """Verifica se a URL é do Google Maps."""
        padrao = r'(maps\.google\.|google\.[a-z]+/maps|goo\.gl/maps)'
        return bool(re.search(padrao, url, re.IGNORECASE))

    def _eh_pagina_busca(self, url: str) -> bool:
        """Verifica se a URL é uma página de busca ou de estabelecimento individual."""
        return '/search/' in url or '/maps/search/' in url

    def extract(self) -> List[Lead]:
        """
        Extrai dados de lead(s) do Google Maps.

        Returns:
            Lista de leads extraídos
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()

            try:
                # Navega para a página
                page.goto(self.url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(3000)  # Aguarda carregamento adicional

                # Verifica se é página de busca ou individual
                if self._eh_pagina_busca(self.url):
                    leads = self._extrair_resultados_busca(page)
                else:
                    lead = self._extrair_estabelecimento_individual(page)
                    leads = [lead] if lead else []

                return leads

            except PlaywrightTimeoutError:
                raise Exception(f"Timeout ao carregar a página: {self.url}")
            except Exception as e:
                raise Exception(f"Erro ao extrair dados do Google Maps: {str(e)}")
            finally:
                browser.close()

    def _extrair_resultados_busca(self, page) -> List[Lead]:
        """Extrai dados de múltiplos estabelecimentos de uma página de busca."""
        leads = []

        # Aguarda a lista de resultados carregar
        try:
            page.wait_for_selector('div[role="feed"]', timeout=10000)
        except:
            return leads

        print("Rolando a página para carregar todos os resultados...")

        # Rola a página até carregar todos os resultados
        tentativas_sem_novos = 0
        contagem_anterior = 0

        while tentativas_sem_novos < 3:
            # Rola até o final do feed
            page.evaluate('document.querySelector(\'div[role="feed"]\').scrollTo(0, document.querySelector(\'div[role="feed"]\').scrollHeight)')
            page.wait_for_timeout(1500)

            # Conta quantos links existem agora
            links_atuais = page.query_selector_all('a[href*="/maps/place/"]')
            contagem_atual = len(links_atuais)

            print(f"  Encontrados {contagem_atual} resultados...")

            # Se não aumentou, incrementa contador
            if contagem_atual == contagem_anterior:
                tentativas_sem_novos += 1
            else:
                tentativas_sem_novos = 0
                contagem_anterior = contagem_atual

        # Encontra todos os links de estabelecimentos
        links = page.query_selector_all('a[href*="/maps/place/"]')

        # Remove duplicatas mantendo ordem
        urls_vistas = set()
        links_unicos = []
        for link in links:
            href = link.get_attribute('href')
            if href and href not in urls_vistas:
                urls_vistas.add(href)
                links_unicos.append(link)

        print(f"\nRolagem completa! Total: {len(links_unicos)} estabelecimentos únicos\n")

        # Aplica limite se especificado
        total_a_extrair = len(links_unicos) if self.limit is None else min(self.limit, len(links_unicos))

        print(f"Extraindo dados de {total_a_extrair} estabelecimento(s)...\n")

        # Extrai dados de cada estabelecimento
        for i, link in enumerate(links_unicos[:total_a_extrair], 1):
            try:
                print(f"[{i}/{total_a_extrair}] Extraindo...")

                # Clica no resultado para abrir os detalhes
                link.scroll_into_view_if_needed()
                page.wait_for_timeout(300)
                link.click()
                page.wait_for_timeout(3000)  # Aguarda detalhes carregarem

                # Aguarda os botões de ação (telefone, website) carregarem
                try:
                    page.wait_for_selector('button[data-item-id], a[data-item-id]', timeout=2000)
                except:
                    pass  # Continua mesmo se não encontrar

                # Extrai nome
                nome = None
                nome_seletores = ['h1.DUwDvf', 'h1', '[class*="fontHeadline"]']
                for seletor in nome_seletores:
                    elem = page.query_selector(seletor)
                    if elem:
                        nome = self._limpar_texto(elem.inner_text())
                        if nome and len(nome) > 3:
                            break

                if not nome:
                    print(f"  ✗ Nome não encontrado")
                    continue

                # Extrai telefone
                telefone = None
                telefone_btn = page.query_selector('button[data-item-id*="phone"]')
                if telefone_btn:
                    tel_attr = telefone_btn.get_attribute('data-item-id')
                    if tel_attr and 'phone:tel:' in tel_attr:
                        telefone = tel_attr.replace('phone:tel:', '').replace('tel:', '')

                # Se não achou pelo botão, procura no conteúdo
                if not telefone:
                    content = page.content()
                    telefone_pattern = r'\(\d{2}\)\s*\d{4,5}[-\s]?\d{4}'
                    match = re.search(telefone_pattern, content)
                    if match:
                        telefone = match.group()

                # Extrai website
                website = self._extrair_website(page)

                # Cria o lead
                lead = Lead(
                    nome=nome,
                    email=None,
                    website=website,
                    telefone=telefone,
                    fonte=self.fonte,
                    url_origem=self.url
                )

                leads.append(lead)
                print(f"  ✓ {nome[:40]} - {telefone or 'Sem telefone'}")

            except Exception as e:
                print(f"  ✗ Erro: {str(e)[:50]}")
                continue

        return leads

    def _extrair_estabelecimento_individual(self, page) -> Lead | None:
        """Extrai dados de um estabelecimento individual."""
        # Extrai o nome do estabelecimento
        nome = self._extrair_nome(page)
        if not nome:
            return None

        # Extrai outros dados
        telefone = self._extrair_telefone(page)
        website = self._extrair_website(page)
        email = self._extrair_email(page)

        # Cria o lead
        lead = Lead(
            nome=nome,
            email=email,
            website=website,
            telefone=telefone,
            fonte=self.fonte,
            url_origem=self.url
        )

        return lead

    def _extrair_nome(self, page) -> Optional[str]:
        """Extrai o nome do estabelecimento."""
        seletores = [
            'h1.DUwDvf',
            'h1[class*="title"]',
            'h1',
            '[data-attrid="title"]',
        ]

        for seletor in seletores:
            try:
                elemento = page.query_selector(seletor)
                if elemento:
                    nome = elemento.inner_text()
                    return self._limpar_texto(nome)
            except:
                continue

        return None

    def _extrair_telefone(self, page) -> Optional[str]:
        """Extrai o telefone do estabelecimento."""
        seletores = [
            'button[data-item-id*="phone"]',
            '[data-tooltip="Copiar número de telefone"]',
            'button[aria-label*="Telefone"]',
            'button[aria-label*="Phone"]',
        ]

        for seletor in seletores:
            try:
                elemento = page.query_selector(seletor)
                if elemento:
                    telefone = elemento.get_attribute('data-item-id')
                    if telefone and 'phone:tel:' in telefone:
                        telefone = telefone.replace('phone:tel:', '')
                        return self._limpar_texto(telefone)

                    # Tenta pegar o texto do elemento
                    telefone = elemento.inner_text()
                    if telefone:
                        return self._limpar_texto(telefone)
            except:
                continue

        # Busca por padrão de telefone no conteúdo da página
        try:
            conteudo = page.content()
            padrao_tel = r'\+?[\d\s\(\)\-]{8,}'
            matches = re.findall(padrao_tel, conteudo)
            if matches:
                return self._limpar_texto(matches[0])
        except:
            pass

        return None

    def _extrair_website(self, page) -> Optional[str]:
        """Extrai o website do estabelecimento."""
        from urllib.parse import urlparse, parse_qs

        seletores = [
            'a[data-item-id*="authority"]',
            'a[aria-label*="Website"]',
            'a[aria-label*="Site"]',
            'a[data-tooltip*="Website"]',
            'a[data-tooltip*="Site"]',
            'button[data-item-id*="authority"]',
            'a[href*="/url?"]',  # Links redirecionados pelo Google
        ]

        for seletor in seletores:
            try:
                elemento = page.query_selector(seletor)
                if elemento:
                    website = elemento.get_attribute('href')
                    if not website:
                        website = elemento.get_attribute('data-item-id')
                        if website and 'authority' in website:
                            website = website.split('authority:')[-1]

                    if website:
                        # Trata URLs redirecionadas pelo Google (/url?q=...)
                        if '/url?' in website and 'q=' in website:
                            try:
                                parsed = urlparse(website)
                                params = parse_qs(parsed.query)
                                if 'q' in params:
                                    website = params['q'][0]
                            except:
                                pass

                        # Valida se é uma URL válida
                        if website.startswith('http'):
                            return self._limpar_texto(website)
            except:
                continue

        return None

    def _extrair_email(self, page) -> Optional[str]:
        """Extrai o email do estabelecimento (se disponível no site)."""
        try:
            # Google Maps raramente mostra email diretamente
            # Procura por padrão de email no conteúdo
            conteudo = page.content()
            padrao_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            matches = re.findall(padrao_email, conteudo)
            if matches:
                # Filtra emails genéricos/spam
                emails_ignorar = ['example.com', 'test.com', 'google.com']
                for email in matches:
                    if not any(ignorar in email.lower() for ignorar in emails_ignorar):
                        return email
        except:
            pass

        return None
