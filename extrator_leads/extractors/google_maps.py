"""Extractor para Google Maps."""

import re
from typing import Optional
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

    def extract(self) -> Optional[Lead]:
        """
        Extrai dados de lead do Google Maps.

        Returns:
            Lead extraído ou None se não encontrado
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
                page.goto(self.url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(2000)  # Aguarda carregamento adicional

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

            except PlaywrightTimeoutError:
                raise Exception(f"Timeout ao carregar a página: {self.url}")
            except Exception as e:
                raise Exception(f"Erro ao extrair dados do Google Maps: {str(e)}")
            finally:
                browser.close()

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
        seletores = [
            'a[data-item-id*="authority"]',
            'a[aria-label*="Website"]',
            'a[aria-label*="Site"]',
            'button[data-item-id*="authority"]',
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

                    if website and website.startswith('http'):
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
