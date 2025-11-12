# Extrator de Leads

Ferramenta CLI para extração de leads de múltiplas plataformas (Google Maps, Facebook, LinkedIn).

## Versão

0.3.1

## Características

- Extração de leads do Google Maps (nome, telefone, email, website)
- Suporte a páginas de busca com rolagem infinita
- Limite configurável de leads a extrair
- Arquitetura expansível para Facebook e LinkedIn (em desenvolvimento)
- Exportação automática para CSV
- Interface CLI intuitiva com Typer
- Output colorido e formatado com Rich

## Requisitos

- Python >= 3.13
- uv (gerenciador de pacotes)

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/marcosf63/extrator-leads.git
cd extrator-leads

# Instalar dependências com uv
uv sync

# Instalar browsers do Playwright
uv run playwright install chromium
```

## Uso

### Extrair lead de uma URL

```bash
# Usar o comando instalado
extrator extract "https://maps.google.com/..."

# Ou executar via uv
uv run extrator extract "https://maps.google.com/..."

# Especificar nome do arquivo de saída
extrator extract "URL" --output meus_leads.csv

# Adicionar a um arquivo existente
extrator extract "URL" --output leads.csv --append

# Limitar número de leads extraídos
extrator extract "URL" --limit 50

# Extrair de uma página de busca do Google Maps
extrator extract "https://www.google.com/maps/search/advogados+sobral" --limit 100
```

### Listar arquivos CSV gerados

```bash
extrator list-files
```

### Ver plataformas suportadas

```bash
extrator platforms
```

### Ver versão

```bash
extrator version
```

## Estrutura do Projeto

```
extrator_leads/
├── extrator_leads/          # Pacote principal
│   ├── cli.py              # Interface CLI
│   ├── core/               # Lógica central
│   │   ├── models.py       # Modelos de dados (Lead)
│   │   ├── extractor_factory.py  # Factory Pattern
│   │   └── csv_exporter.py # Exportação CSV
│   └── extractors/         # Extractors por plataforma
│       ├── base.py         # Classe base abstrata
│       ├── google_maps.py  # Google Maps (implementado)
│       ├── facebook.py     # Facebook (em desenvolvimento)
│       └── linkedin.py     # LinkedIn (em desenvolvimento)
├── data/                   # CSVs gerados
├── tests/                  # Testes
└── main.py                 # Entry point
```

## Desenvolvimento

Este projeto usa `uv` para gerenciamento de dependências.

```bash
# Adicionar nova dependência
uv add nome-do-pacote

# Adicionar dependência de desenvolvimento
uv add --dev nome-do-pacote

# Sincronizar dependências
uv sync

# Executar testes (quando implementados)
uv run pytest
```

## Plataformas Suportadas

| Plataforma | Status | Descrição |
|------------|--------|-----------|
| Google Maps | ✅ Disponível | Extração completa de dados |
| Facebook | 🚧 Em desenvolvimento | Planejado para versão futura |
| LinkedIn | 🚧 Em desenvolvimento | Planejado para versão futura |

## Tecnologias

- **Typer**: Framework CLI moderno
- **Rich**: Output formatado no terminal
- **Pydantic**: Validação de dados
- **Playwright**: Automação web
- **Pandas**: Manipulação de dados e CSV

## Licença

MIT

## Autor

Marcos <marcosf63@gmail.com>
