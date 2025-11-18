import pytest
from extrator_leads.core.extractor_factory import ExtractorFactory
from extrator_leads.extractors.google_maps import GoogleMapsExtractor

def test_factory_google_maps():
    """Testa criação de extractor do Google Maps."""
    url = "https://www.google.com/maps/search/restaurantes"
    extractor = ExtractorFactory.criar_extractor(url)
    assert isinstance(extractor, GoogleMapsExtractor)
    assert extractor.url == url

def test_factory_url_invalida():
    """Testa erro ao passar URL não suportada."""
    url = "https://www.site-aleatorio.com"
    with pytest.raises(ValueError) as excinfo:
        ExtractorFactory.criar_extractor(url)
    assert "URL não suportada" in str(excinfo.value)

def test_factory_callback():
    """Testa se o callback é passado corretamente."""
    def my_callback(msg):
        pass
        
    url = "https://www.google.com/maps/search/restaurantes"
    extractor = ExtractorFactory.criar_extractor(url, callback=my_callback)
    assert extractor.callback == my_callback
