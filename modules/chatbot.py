"""
modules/chatbot.py
Módulo responsável por carregar o modelo de linguagem (LLM) e gerar respostas
do Tutor Virtual Inteligente.
Compatível com:
- OpenAI (via langchain-openai)
- Mistral (via langchain-mistralai)
"""

import os
from dotenv import load_dotenv

# Importações principais do LangChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# Carregar variáveis de ambiente (.env)
load_dotenv()

# =======================================================================
# 🔧 FUNÇÃO: Carregar modelo de linguagem
# =======================================================================
def load_llm(modelo: str = "Mistral"):
    """
    Carrega o modelo de linguagem de acordo com a escolha do usuário.
    Aceita: "Mistral" ou "OpenAI GPT-4"
    """

    if modelo == "OpenAI GPT-4":
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("❌ Chave API da OpenAI não encontrada. Defina OPENAI_API_KEY no arquivo .env.")

        print("🔹 Carregando modelo OpenAI GPT-4...")
        return ChatOpenAI( 
            model="gpt-4o-mini",  # modelo leve, rápido e eficiente
            temperature=0.6,
            api_key=api_key
        )

    elif modelo == "Mistral":
        from langchain_mistralai import ChatMistralAI
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            raise ValueError("❌ Chave API da Mistral não encontrada. Defina MISTRAL_API_KEY no arquivo .env.")

        print("🔹 Carregando modelo Mistral...")
        return ChatMistralAI(
            model="mistral-large-latest",  # modelo atual da Mistral
            temperature=0.6,
            api_key=api_key
        )

    else:
        raise ValueError(f"Modelo desconhecido: {modelo}. Use 'Mistral' ou 'OpenAI GPT-4'.")


# =======================================================================
# 🧩 FUNÇÃO: Gerar resposta do chatbot
# =======================================================================
def gerar_resposta(pergunta: str, llm=None):
    """
    Gera uma resposta textual para a pergunta do usuário.
    Se nenhum LLM for passado, usa o modelo padrão (Mistral).
    """

    if llm is None:
        llm = load_llm("Mistral")

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=(
            "És um tutor virtual educacional especializado em ajudar alunos. "
            "Explica conceitos com clareza, dá exemplos e adapta o tom conforme a dificuldade."
        )),
        HumanMessage(content=pergunta)
    ])

    # Geração da resposta
    resposta = llm.invoke(prompt.format_messages())

    # Retorna o texto puro da resposta
    return resposta.content.strip()
