"""Extractor para LinkedIn (em desenvolvimento)."""

import re
from typing import Optional
from extrator_leads.extractors.base import BaseExtractor
from extrator_leads.core.models import Lead


class LinkedInExtractor(BaseExtractor):
    """Extractor de leads do LinkedIn (em desenvolvimento)."""

    @property
    def fonte(self) -> str:
        """Retorna o nome da fonte."""
        return "linkedin"

    @classmethod
    def pode_extrair(cls, url: str) -> bool:
        """Verifica se a URL é do LinkedIn."""
        padrao = r'linkedin\.com'
        return bool(re.search(padrao, url, re.IGNORECASE))

    def extract(self) -> Optional[Lead]:
        """
        Extrai dados de lead do LinkedIn.

        Returns:
            Lead extraído ou None se não encontrado

        Raises:
            NotImplementedError: Esta funcionalidade ainda não foi implementada
        """
        raise NotImplementedError(
            "Extração de leads do LinkedIn ainda não foi implementada. "
            "Esta funcionalidade será adicionada em versões futuras."
        )
