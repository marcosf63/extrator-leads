"""Extractor para Facebook (em desenvolvimento)."""

import re
from typing import Optional
from extrator_leads.extractors.base import BaseExtractor
from extrator_leads.core.models import Lead


class FacebookExtractor(BaseExtractor):
    """Extractor de leads do Facebook (em desenvolvimento)."""

    @property
    def fonte(self) -> str:
        """Retorna o nome da fonte."""
        return "facebook"

    @classmethod
    def pode_extrair(cls, url: str) -> bool:
        """Verifica se a URL é do Facebook."""
        padrao = r'(facebook\.com|fb\.com|fb\.me)'
        return bool(re.search(padrao, url, re.IGNORECASE))

    def extract(self) -> Optional[Lead]:
        """
        Extrai dados de lead do Facebook.

        Returns:
            Lead extraído ou None se não encontrado

        Raises:
            NotImplementedError: Esta funcionalidade ainda não foi implementada
        """
        raise NotImplementedError(
            "Extração de leads do Facebook ainda não foi implementada. "
            "Esta funcionalidade será adicionada em versões futuras."
        )
