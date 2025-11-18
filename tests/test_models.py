import pytest
from extrator_leads.core.models import Lead

def test_lead_validacao_telefone():
    """Testa validação e normalização de telefone."""
    # Caso válido
    assert Lead.validar_telefone("+55 11 99999-9999") == "+5511999999999"
    assert Lead.validar_telefone("(11) 99999-9999") == "11999999999"
    
    # Caso inválido (muito curto)
    assert Lead.validar_telefone("123") is None
    
    # Caso None
    assert Lead.validar_telefone(None) is None

def test_lead_validacao_nome():
    """Testa validação de nome."""
    # Caso válido
    assert Lead.validar_nome("  Empresa Teste  ") == "Empresa Teste"
    
    # Caso inválido (vazio)
    with pytest.raises(ValueError):
        Lead.validar_nome("")
    
    with pytest.raises(ValueError):
        Lead.validar_nome("   ")

def test_lead_to_dict():
    """Testa conversão para dicionário."""
    lead = Lead(
        nome="Empresa Teste",
        email="contato@teste.com",
        website="https://teste.com",
        telefone="+55 11 99999-9999",
        fonte="google_maps",
        url_origem="https://maps.google.com"
    )
    
    data = lead.to_dict()
    assert data['nome'] == "Empresa Teste"
    assert data['email'] == "contato@teste.com"
    assert data['website'] == "https://teste.com/"
    assert data['telefone'] == "+5511999999999"  # Normalizado
    assert data['fonte'] == "google_maps"
