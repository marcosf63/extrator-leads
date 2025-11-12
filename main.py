"""Entry point para o CLI de extração de leads."""

import logging
from extrator_leads.cli import app


def main():
    """Função principal que inicializa o CLI."""
    # Configura logging básico
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Executa o CLI
    app()


if __name__ == "__main__":
    main()
