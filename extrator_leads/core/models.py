"""Modelos de dados para leads."""

from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator
import re


class Lead(BaseModel):
    """Modelo para representar um lead extraído."""

    nome: str
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    telefone: Optional[str] = None
    fonte: str  # google_maps, facebook, linkedin
    url_origem: str

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza o número de telefone."""
        if v is None:
            return None

        # Remove caracteres não numéricos exceto + no início
        telefone_limpo = re.sub(r'[^\d+]', '', v)

        # Verifica se tem pelo menos 8 dígitos (mínimo para um telefone válido)
        digitos = re.sub(r'\D', '', telefone_limpo)
        if len(digitos) < 8:
            return None

        return telefone_limpo

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        """Valida que o nome não está vazio."""
        if not v or not v.strip():
            raise ValueError("Nome não pode estar vazio")
        return v.strip()

    def to_dict(self) -> dict:
        """Converte o lead para dicionário, formatando URLs."""
        data = {
            'nome': self.nome,
            'email': self.email,
            'website': str(self.website) if self.website else None,
            'telefone': self.telefone,
            'fonte': self.fonte,
            'url_origem': self.url_origem
        }
        return data

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome": "Empresa Exemplo",
                "email": "contato@exemplo.com",
                "website": "https://exemplo.com",
                "telefone": "+55 11 98765-4321",
                "fonte": "google_maps",
                "url_origem": "https://maps.google.com/example"
            }
        }
    }
