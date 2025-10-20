"""
utils/helpers.py
Funções utilitárias para o sistema RAG — listagem e verificação de PDFs.
"""

import os

def listar_pdfs(diretorio="data/docs"):
    """
    Lista todos os arquivos PDF válidos dentro do diretório especificado.
    Cria o diretório caso não exista.
    
    Retorna:
        - Lista de caminhos completos dos PDFs encontrados.
        - Lista vazia se nenhum arquivo for encontrado.
    """
    # Lista apenas PDFs válidos (ignora .PDF/.Pdf etc)
    pdfs = [
        os.path.join(diretorio, f)
        for f in os.listdir(diretorio)
        if f.lower().endswith(".pdf") and os.path.isfile(os.path.join(diretorio, f))
    ]

    if not pdfs:
        print("⚠️ Nenhum arquivo PDF encontrado em:", diretorio)
    else:
        print(f"📄 {len(pdfs)} arquivo(s) PDF encontrado(s):")
        for pdf in pdfs:
            print(f"   - {os.path.basename(pdf)}")

    return pdfs
