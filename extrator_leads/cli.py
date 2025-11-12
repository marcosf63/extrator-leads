"""Interface CLI para extração de leads."""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from extrator_leads.core.extractor_factory import ExtractorFactory
from extrator_leads.core.csv_exporter import CSVExporter

app = typer.Typer(
    name="extrator",
    help="Ferramenta CLI para extração de leads de múltiplas plataformas",
    add_completion=False
)
console = Console()


@app.command()
def extract(
    url: str = typer.Argument(..., help="URL da página para extrair leads"),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Nome do arquivo CSV de saída (opcional, gera automaticamente se não fornecido)"
    ),
    append: bool = typer.Option(
        False,
        "--append",
        "-a",
        help="Adicionar ao arquivo existente ao invés de sobrescrever"
    ),
    output_dir: str = typer.Option(
        "data",
        "--output-dir",
        "-d",
        help="Diretório onde o CSV será salvo"
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        "-l",
        help="Número máximo de leads a extrair (padrão: todos os disponíveis)"
    )
):
    """
    Extrai dados de lead de uma URL e salva em CSV.

    Exemplo:
        extrator extract "https://maps.google.com/..."
    """
    console.print(f"\n[bold cyan]Extrator de Leads v0.3.3[/bold cyan]\n")

    try:
        # Cria o extractor apropriado
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(description="Analisando URL...", total=None)

            try:
                extractor = ExtractorFactory.criar_extractor(url, limit=limit)
            except ValueError as e:
                console.print(f"\n[bold red]Erro:[/bold red] {str(e)}\n")
                raise typer.Exit(code=1)

            console.print(f"[green]✓[/green] Plataforma detectada: [bold]{extractor.fonte}[/bold]\n")

            # Extrai dados
            progress.add_task(description=f"Extraindo dados de {extractor.fonte}...", total=None)

            try:
                leads = extractor.extract()
            except NotImplementedError as e:
                console.print(f"\n[bold yellow]Aviso:[/bold yellow] {str(e)}\n")
                raise typer.Exit(code=1)
            except Exception as e:
                console.print(f"\n[bold red]Erro na extração:[/bold red] {str(e)}\n")
                raise typer.Exit(code=1)

            if not leads:
                console.print("\n[bold yellow]Nenhum lead encontrado na URL fornecida.[/bold yellow]\n")
                raise typer.Exit(code=1)

        # Exibe dados extraídos
        console.print(f"[green]✓[/green] {len(leads)} lead(s) extraído(s) com sucesso!\n")

        if len(leads) == 1:
            _exibir_lead(leads[0])
        else:
            _exibir_leads_tabela(leads)

        # Exporta para CSV
        exporter = CSVExporter(output_dir=output_dir)

        try:
            caminho = exporter.exportar(leads, filename=output, append=append)
            console.print(f"\n[green]✓[/green] {len(leads)} lead(s) salvo(s) em: [bold]{caminho}[/bold]\n")
        except Exception as e:
            console.print(f"\n[bold red]Erro ao salvar CSV:[/bold red] {str(e)}\n")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Operação cancelada pelo usuário.[/yellow]\n")
        raise typer.Exit(code=130)
    except Exception as e:
        console.print(f"\n[bold red]Erro inesperado:[/bold red] {str(e)}\n")
        raise typer.Exit(code=1)


@app.command()
def list_files(
    output_dir: str = typer.Option(
        "data",
        "--output-dir",
        "-d",
        help="Diretório para listar arquivos"
    )
):
    """
    Lista todos os arquivos CSV gerados.
    """
    console.print(f"\n[bold cyan]Arquivos CSV em {output_dir}/[/bold cyan]\n")

    exporter = CSVExporter(output_dir=output_dir)
    arquivos = exporter.listar_arquivos()

    if not arquivos:
        console.print("[yellow]Nenhum arquivo CSV encontrado.[/yellow]\n")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=6)
    table.add_column("Arquivo")

    for idx, arquivo in enumerate(arquivos, 1):
        caminho_completo = Path(output_dir) / arquivo
        size = caminho_completo.stat().st_size if caminho_completo.exists() else 0
        size_kb = size / 1024
        table.add_row(str(idx), f"{arquivo} ({size_kb:.1f} KB)")

    console.print(table)
    console.print()


@app.command()
def platforms():
    """
    Lista as plataformas suportadas para extração de leads.
    """
    console.print("\n[bold cyan]Plataformas Suportadas[/bold cyan]\n")

    plataformas_info = [
        ("Google Maps", "google_maps", "✓ Disponível", "green"),
        ("Facebook", "facebook", "⚠ Em desenvolvimento", "yellow"),
        ("LinkedIn", "linkedin", "⚠ Em desenvolvimento", "yellow"),
    ]

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Plataforma", style="cyan", width=20)
    table.add_column("ID", style="dim")
    table.add_column("Status", width=25)

    for nome, id_plat, status, cor in plataformas_info:
        table.add_row(nome, id_plat, f"[{cor}]{status}[/{cor}]")

    console.print(table)
    console.print()


@app.command()
def version():
    """
    Exibe a versão do extrator.
    """
    console.print("\n[bold cyan]Extrator de Leads[/bold cyan]")
    console.print("Versão: [bold]0.3.3[/bold]")
    console.print("Autor: Marcos <marcosf63@gmail.com>\n")


def _exibir_lead(lead):
    """Exibe os dados do lead em uma tabela."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Campo", style="cyan", width=15)
    table.add_column("Valor", style="white")

    table.add_row("Nome", lead.nome or "[dim]N/A[/dim]")
    table.add_row("Telefone", lead.telefone or "[dim]N/A[/dim]")
    table.add_row("Email", lead.email or "[dim]N/A[/dim]")
    table.add_row("Website", str(lead.website) if lead.website else "[dim]N/A[/dim]")
    table.add_row("Fonte", lead.fonte)

    console.print(table)


def _exibir_leads_tabela(leads):
    """Exibe múltiplos leads em uma tabela compacta."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Nome", style="cyan")
    table.add_column("Telefone", style="green")
    table.add_column("Website", style="blue")

    for idx, lead in enumerate(leads, 1):
        table.add_row(
            str(idx),
            lead.nome[:40] + "..." if len(lead.nome) > 40 else lead.nome,
            lead.telefone or "[dim]N/A[/dim]",
            str(lead.website)[:30] + "..." if lead.website and len(str(lead.website)) > 30 else (str(lead.website) if lead.website else "[dim]N/A[/dim]")
        )

    console.print(table)


if __name__ == "__main__":
    app()
