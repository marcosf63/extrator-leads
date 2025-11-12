"""Exportador de leads para CSV."""

import os
from datetime import datetime
from pathlib import Path
from typing import List
import pandas as pd
from extrator_leads.core.models import Lead


class CSVExporter:
    """Classe para exportar leads para arquivos CSV."""

    def __init__(self, output_dir: str = "data"):
        """
        Inicializa o exportador.

        Args:
            output_dir: Diretório onde os CSVs serão salvos
        """
        self.output_dir = Path(output_dir)
        self._garantir_diretorio()

    def _garantir_diretorio(self) -> None:
        """Garante que o diretório de saída existe."""
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _gerar_nome_arquivo(self, custom_name: str = None) -> str:
        """
        Gera nome do arquivo CSV.

        Args:
            custom_name: Nome customizado (opcional)

        Returns:
            Nome do arquivo
        """
        if custom_name:
            if not custom_name.endswith('.csv'):
                custom_name += '.csv'
            return custom_name

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"leads_{timestamp}.csv"

    def exportar(
        self,
        leads: List[Lead],
        filename: str = None,
        append: bool = False
    ) -> str:
        """
        Exporta lista de leads para CSV.

        Args:
            leads: Lista de leads para exportar
            filename: Nome do arquivo (opcional, gera automaticamente se não fornecido)
            append: Se True, adiciona ao arquivo existente ao invés de sobrescrever

        Returns:
            Caminho completo do arquivo gerado

        Raises:
            ValueError: Se a lista de leads estiver vazia
        """
        if not leads:
            raise ValueError("Lista de leads está vazia")

        # Converte leads para dicionários
        dados = [lead.to_dict() for lead in leads]

        # Cria DataFrame
        df = pd.DataFrame(dados)

        # Define colunas na ordem desejada
        colunas = ['nome', 'telefone', 'email', 'website', 'fonte', 'url_origem']
        df = df[colunas]

        # Gera nome do arquivo
        nome_arquivo = self._gerar_nome_arquivo(filename)
        caminho_completo = self.output_dir / nome_arquivo

        # Exporta para CSV
        if append and caminho_completo.exists():
            # Append ao arquivo existente
            df.to_csv(
                caminho_completo,
                mode='a',
                header=False,
                index=False,
                encoding='utf-8'
            )
        else:
            # Cria novo arquivo ou sobrescreve
            df.to_csv(
                caminho_completo,
                index=False,
                encoding='utf-8'
            )

        return str(caminho_completo)

    def exportar_lead(
        self,
        lead: Lead,
        filename: str = None,
        append: bool = False
    ) -> str:
        """
        Exporta um único lead para CSV.

        Args:
            lead: Lead para exportar
            filename: Nome do arquivo (opcional)
            append: Se True, adiciona ao arquivo existente

        Returns:
            Caminho completo do arquivo gerado
        """
        return self.exportar([lead], filename, append)

    def listar_arquivos(self) -> List[str]:
        """
        Lista todos os arquivos CSV no diretório de saída.

        Returns:
            Lista de nomes de arquivos
        """
        if not self.output_dir.exists():
            return []

        arquivos = list(self.output_dir.glob("*.csv"))
        return [arquivo.name for arquivo in sorted(arquivos, reverse=True)]

    def obter_caminho_completo(self, filename: str) -> str:
        """
        Obtém o caminho completo para um arquivo.

        Args:
            filename: Nome do arquivo

        Returns:
            Caminho completo
        """
        return str(self.output_dir / filename)
