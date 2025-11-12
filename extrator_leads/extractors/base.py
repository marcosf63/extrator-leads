"""Classe base abstrata para extractors de leads."""

from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse
from extrator_leads.core.models import Lead


class BaseExtractor(ABC):
    """Classe base para todos os extractors de leads."""

    def __init__(self, url: str):
        """
        Inicializa o extractor.

        Args:
            url: URL da página para extrair dados
        """
        self.url = url
        self._validar_url()

    def _validar_url(self) -> None:
        """Valida se a URL está no formato correto."""
        try:
            resultado = urlparse(self.url)
            if not all([resultado.scheme, resultado.netloc]):
                raise ValueError(f"URL inválida: {self.url}")
        except Exception as e:
            raise ValueError(f"Erro ao validar URL: {str(e)}")

    @abstractmethod
    def extract(self) -> Optional[Lead]:
        """
        Extrai dados de lead da URL.

        Returns:
            Lead extraído ou None se não encontrado

        Raises:
            Exception: Se houver erro na extração
        """
        pass

    @property
    @abstractmethod
    def fonte(self) -> str:
        """
        Retorna o nome da fonte (plataforma).

        Returns:
            Nome da plataforma (ex: 'google_maps', 'facebook', 'linkedin')
        """
        pass

    @classmethod
    @abstractmethod
    def pode_extrair(cls, url: str) -> bool:
        """
        Verifica se este extractor pode processar a URL.

        Args:
            url: URL para verificar

        Returns:
            True se pode processar, False caso contrário
        """
        pass

    def _limpar_texto(self, texto: Optional[str]) -> Optional[str]:
        """
        Limpa e normaliza texto extraído.

        Args:
            texto: Texto para limpar

        Returns:
            Texto limpo ou None
        """
        if not texto:
            return None

        texto_limpo = texto.strip()
        return texto_limpo if texto_limpo else None
