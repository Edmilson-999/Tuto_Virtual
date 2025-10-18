"""
Módulo: chatbot.py
------------------
Gerencia a comunicação com o modelo de linguagem (OpenAI ou Mistral)
para o Tutor Virtual Inteligente.
"""

import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Variáveis do ambiente
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai").lower()

# Imports condicionais
if MODEL_PROVIDER == "mistral":
    from langchain_mistralai import ChatMistralAI
else:
    from langchain_openai import ChatOpenAI


def load_llm():
    """
    Inicializa o modelo LLM conforme o provedor definido no .env.
    """

    if MODEL_PROVIDER == "mistral":
        if not MISTRAL_KEY:
            raise ValueError("❌ MISTRAL_API_KEY não foi encontrada no .env")

        print("✅ Usando modelo da Mistral")
        llm = ChatMistralAI(
            model=os.getenv("MISTRAL_MODEL", "mistral-small"),
            api_key=MISTRAL_KEY,
            temperature=0.7
        )

    else:
        if not OPENAI_KEY:
            raise ValueError("❌ OPENAI_API_KEY não foi encontrada no .env")

        print("✅ Usando modelo da OpenAI")
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=OPENAI_KEY,
            temperature=0.7
        )

    return llm


def get_response(llm, user_input):
    """
    Gera uma resposta do chatbot.
    """
    try:
        response = llm.invoke(user_input)
        return response.content
    except Exception as e:
        return f"Ocorreu um erro ao processar a resposta: {str(e)}"
