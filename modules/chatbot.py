# modules/chatbot.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Inicializar o modelo da OpenAI (conversa geral)
llm = ChatOpenAI(
    model="gpt-4o-mini",       # podes usar "gpt-4-turbo" se preferires
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def gerar_resposta(pergunta: str) -> str:
    """
    Gera uma resposta com base na pergunta do usuário.
    """
    if not pergunta:
        return "Por favor, digite uma pergunta."

    # Template de prompt
    prompt = ChatPromptTemplate.from_template(
        "És um tutor virtual educacional. Responde de forma clara, paciente e explicativa à seguinte pergunta: {pergunta}"
    )

    mensagens = prompt.format_messages(pergunta=pergunta)
    resposta = llm.invoke(mensagens)
    return resposta.content
