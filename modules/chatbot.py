# modules/chatbot.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o modelo (GPT-4, pode trocar por outro)
llm = ChatOpenAI(
    model="gpt-4-turbo",  # ou "gpt-3.5-turbo"
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def gerar_resposta(pergunta: str) -> str:
    """
    Gera uma resposta com base na pergunta do usuário.
    """
    if not pergunta:
        return "Por favor, digite uma pergunta."

    prompt = ChatPromptTemplate.from_template(
        "És um tutor virtual educacional. Responde de forma clara e explicativa à pergunta: {pergunta}"
    )

    mensagens = prompt.format_messages(pergunta=pergunta)
    resposta = llm(mensagens)
    return resposta.content
