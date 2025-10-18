import os
import subprocess

# Versões testadas e compatíveis entre si
packages = {
    "langchain": "0.3.27",
    "langchain-core": "0.3.78",
    "langchain-community": "0.3.15",
    "langchain-openai": "0.3.35",
    "langchain-mistralai": "0.2.3",
    "langchain-chroma": "0.1.4",
    "chromadb": "",
    "streamlit": "",
    "pypdf": "",
    "python-dotenv": "",
}

print("🔍 Corrigindo versões dos pacotes LangChain e dependências...\n")

for pkg, version in packages.items():
    if version:
        cmd = f"pip install {pkg}=={version} --quiet"
    else:
        cmd = f"pip install {pkg} --quiet"

    print(f"➡️ Instalando {pkg}{'=='+version if version else ''} ...")
    subprocess.call(cmd, shell=True)

print("\n✅ Tudo pronto! Versões compatíveis foram instaladas com sucesso.")
print("👉 Agora podes executar novamente o teu projeto com:  streamlit run app.py")
