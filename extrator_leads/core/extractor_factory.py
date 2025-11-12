"""Factory para criar extractors baseado na URL."""

from typing import Type
from extrator_leads.extractors.base import BaseExtractor
from extrator_leads.extractors.google_maps import GoogleMapsExtractor
from extrator_leads.extractors.facebook import FacebookExtractor
from extrator_leads.extractors.linkedin import LinkedInExtractor


class ExtractorFactory:
    """Factory para criar o extractor apropriado baseado na URL."""

    # Lista de extractors disponíveis (ordem importa - primeiro match ganha)
    _extractors: list[Type[BaseExtractor]] = [
        GoogleMapsExtractor,
        FacebookExtractor,
        LinkedInExtractor,
    ]

    @classmethod
    def criar_extractor(cls, url: str) -> BaseExtractor:
        """
        Cria o extractor apropriado baseado na URL.

        Args:
            url: URL para extrair dados

        Returns:
            Instância do extractor apropriado

        Raises:
            ValueError: Se nenhum extractor suportar a URL
        """
        for extractor_class in cls._extractors:
            if extractor_class.pode_extrair(url):
                return extractor_class(url)

        # Nenhum extractor encontrado
        plataformas_suportadas = [
            "Google Maps (maps.google.com)",
            "Facebook (facebook.com) - em desenvolvimento",
            "LinkedIn (linkedin.com) - em desenvolvimento"
        ]
        mensagem = (
            f"URL não suportada: {url}\n\n"
            f"Plataformas suportadas:\n" +
            "\n".join(f"  - {p}" for p in plataformas_suportadas)
        )
        raise ValueError(mensagem)

    @classmethod
    def plataformas_suportadas(cls) -> list[str]:
        """
        Retorna lista de plataformas suportadas.

        Returns:
            Lista de nomes das plataformas
        """
        plataformas = []
        for extractor_class in cls._extractors:
            # Cria instância temporária para acessar o nome da fonte
            try:
                temp_instance = extractor_class("http://example.com")
                plataformas.append(temp_instance.fonte)
            except:
                pass
        return plataformas
