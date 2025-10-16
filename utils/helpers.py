# utils/helpers.py
import os

def listar_pdfs(diretorio="data/docs"):
    """
    Lista todos os arquivos PDF dentro do diretório especificado.
    """
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    return [f for f in os.listdir(diretorio) if f.endswith(".pdf")]
