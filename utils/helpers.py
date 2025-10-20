"""
utils/helpers.py
Funções auxiliares corrigidas para paths do Windows
"""

import os

def listar_pdfs(diretorio="data/docs"):
    """
    Lista todos os arquivos PDF dentro do diretório especificado.
    Retorna apenas os nomes dos arquivos, não caminhos completos.
    """
    if not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)
        return []
    
    # Listar apenas nomes de arquivos, não caminhos completos
    pdfs = [f for f in os.listdir(diretorio) if f.lower().endswith('.pdf')]
    return pdfs

def get_caminho_pdf(nome_arquivo, diretorio="data/docs"):
    """
    Retorna o caminho completo correto para um arquivo PDF.
    """
    return os.path.join(diretorio, nome_arquivo)

def verificar_pdf_valido(caminho_pdf):
    """
    Verifica se um arquivo PDF existe e é válido.
    """
    return os.path.exists(caminho_pdf) and os.path.isfile(caminho_pdf) and caminho_pdf.lower().endswith('.pdf')