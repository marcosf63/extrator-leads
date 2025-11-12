# Extrator de Leads - Documentação do Projeto

## Informações Gerais

- **Nome do Projeto**: extrator-leads
- **Versão Atual**: 0.1.0
- **Versionamento**: Semantic Versioning (https://semver.org/)
- **Autor**: Marcos <marcosf63@gmail.com>
- **Licença**: MIT

## Estrutura do Projeto

```
extrator_leads/
├── .git/                 # Repositório Git
├── .gitignore           # Arquivos ignorados pelo Git
├── .python-version      # Versão do Python (gerenciada pelo uv)
├── .venv/               # Ambiente virtual (não versionado)
├── main.py              # Arquivo principal da aplicação
├── pyproject.toml       # Configuração do projeto e dependências
├── README.md            # Documentação do usuário
└── CLAUDE.md            # Este arquivo - documentação do projeto
```

## Tecnologias

- **Python**: >= 3.13
- **Gerenciador de Pacotes**: uv (https://github.com/astral-sh/uv)
- **Controle de Versão**: Git

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

## Histórico de Versões

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
