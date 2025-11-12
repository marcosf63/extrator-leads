# Extrator de Leads - Documentação do Projeto

## Informações Gerais

- **Nome do Projeto**: extrator-leads
- **Versão Atual**: 0.2.0
- **Versionamento**: Semantic Versioning (https://semver.org/)
- **Autor**: Marcos <marcosf63@gmail.com>
- **Licença**: MIT
- **Descrição**: Ferramenta CLI para extração de leads de múltiplas plataformas

## Estrutura do Projeto

```
extrator_leads/
├── .git/                      # Repositório Git
├── .gitignore                 # Arquivos ignorados pelo Git
├── .python-version            # Versão do Python (gerenciada pelo uv)
├── .venv/                     # Ambiente virtual (não versionado)
├── .env.example               # Exemplo de variáveis de ambiente
├── extrator_leads/            # Pacote principal
│   ├── __init__.py
│   ├── cli.py                 # Interface CLI com Typer
│   ├── core/                  # Lógica central
│   │   ├── __init__.py
│   │   ├── models.py          # Modelos de dados (Lead)
│   │   ├── extractor_factory.py  # Factory Pattern
│   │   └── csv_exporter.py    # Exportação para CSV
│   ├── extractors/            # Extractors por plataforma
│   │   ├── __init__.py
│   │   ├── base.py            # Classe base abstrata
│   │   ├── google_maps.py     # Google Maps (implementado)
│   │   ├── facebook.py        # Facebook (stub)
│   │   └── linkedin.py        # LinkedIn (stub)
│   └── utils/                 # Utilitários
│       └── __init__.py
├── data/                      # CSVs gerados (não versionado)
├── tests/                     # Testes
│   └── __init__.py
├── main.py                    # Entry point
├── pyproject.toml             # Configuração do projeto
├── README.md                  # Documentação do usuário
└── CLAUDE.md                  # Este arquivo
```

## Tecnologias

- **Python**: >= 3.13
- **Gerenciador de Pacotes**: uv (https://github.com/astral-sh/uv)
- **Controle de Versão**: Git
- **CLI Framework**: Typer 0.20+
- **Terminal UI**: Rich 14.2+
- **Validação de Dados**: Pydantic 2.12+
- **Web Scraping**: Playwright 1.56+
- **Data Processing**: Pandas 2.3+

## Gerenciamento de Dependências

Este projeto usa **uv** para gerenciamento de pacotes e ambientes virtuais.

### Comandos Úteis

```bash
# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Adicionar dependência
uv add nome-do-pacote

# Adicionar dependência de desenvolvimento
uv add --dev nome-do-pacote

# Sincronizar dependências
uv sync

# Executar script
uv run python main.py
```

## Arquitetura

### Padrões de Design

1. **Strategy Pattern**: Classe base `BaseExtractor` com implementações específicas por plataforma
2. **Factory Pattern**: `ExtractorFactory` decide qual extractor usar baseado na URL
3. **Data Transfer Objects**: Modelos Pydantic para validação e serialização

### Fluxo de Execução

1. Usuário executa comando CLI: `extrator extract <url>`
2. CLI valida argumentos e chama `ExtractorFactory`
3. Factory identifica a plataforma pela URL e retorna o extractor apropriado
4. Extractor usa Playwright para acessar a página e extrair dados
5. Dados são validados via modelo Pydantic `Lead`
6. `CSVExporter` salva o lead em arquivo CSV na pasta `data/`
7. CLI exibe resultado formatado com Rich

### Comandos CLI

- `extrator extract <url>`: Extrai lead de uma URL
- `extrator list-files`: Lista CSVs gerados
- `extrator platforms`: Mostra plataformas suportadas
- `extrator version`: Exibe versão

## Histórico de Versões

### 0.2.0 (2025-11-12)
- **feat**: Implementação completa do CLI com Typer
- **feat**: Extractor do Google Maps com Playwright
- **feat**: Sistema de exportação para CSV
- **feat**: Factory Pattern para extensibilidade
- **feat**: Modelos de dados com Pydantic
- **feat**: Stubs para Facebook e LinkedIn
- **arch**: Arquitetura escalável baseada em Strategy Pattern
- **deps**: Instalação de dependências (typer, rich, pydantic, playwright, pandas)
- **docs**: Documentação completa (README.md e CLAUDE.md)

### 0.1.0 (2025-11-12)
- Inicialização do projeto com uv
- Estrutura básica criada
- Configuração inicial do Git
- Documentação básica (README.md e CLAUDE.md)

## Convenções de Commit

Este projeto segue as convenções do Conventional Commits:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças na documentação
- `style:` - Formatação, ponto e vírgula faltando, etc
- `refactor:` - Refatoração de código
- `test:` - Adição ou correção de testes
- `chore:` - Atualizações de build, configs, etc

## Versionamento Semântico

O projeto segue Semantic Versioning:

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (0.X.0): Nova funcionalidade mantendo compatibilidade
- **PATCH** (0.0.X): Correções de bugs mantendo compatibilidade

## Notas de Desenvolvimento

- O ambiente virtual (`.venv/`) não é versionado
- Use sempre `uv` para gerenciar dependências
- Mantenha o README.md atualizado com mudanças significativas
- Atualize este arquivo (CLAUDE.md) a cada nova versão
- Antes de fazer commit, execute `uv sync` para garantir dependências atualizadas
- Para adicionar suporte a novas plataformas:
  1. Criar nova classe em `extrator_leads/extractors/` herdando de `BaseExtractor`
  2. Implementar métodos `extract()`, `fonte`, e `pode_extrair()`
  3. Adicionar a classe em `ExtractorFactory._extractors`
- Os CSVs gerados são salvos em `data/` com timestamp automático
- Use `.env` para configurações locais (baseado em `.env.example`)

## Próximos Passos

### Para v0.3.0
- [ ] Implementar extractor do Facebook
- [ ] Implementar extractor do LinkedIn
- [ ] Adicionar testes unitários com pytest
- [ ] Adicionar opção de extração em lote (múltiplas URLs)
- [ ] Implementar cache de resultados
- [ ] Adicionar suporte a outros formatos de exportação (JSON, Excel)

### Para v0.4.0
- [ ] Interface web simples com FastAPI
- [ ] Sistema de agendamento de extrações
- [ ] Integração com banco de dados
- [ ] API REST para integração com outros sistemas
