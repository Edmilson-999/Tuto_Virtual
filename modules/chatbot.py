"""
modules/chatbot.py
Chatbot com sistema de memória corrigido
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

# =======================================================================
# 🔧 FUNÇÃO: Carregar modelo de linguagem
# =======================================================================
def load_llm(modelo: str = "Mistral"):
    """
    Carrega o modelo de linguagem de acordo com a escolha do usuário.
    """
    if modelo == "OpenAI GPT-4":
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ Chave API da OpenAI não encontrada.")
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.6, api_key=api_key)

    elif modelo == "Mistral":
        from langchain_mistralai import ChatMistralAI
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("❌ Chave API da Mistral não encontrada.")
        return ChatMistralAI(model="mistral-small-latest", temperature=0.6, api_key=api_key)

    else:
        raise ValueError(f"Modelo desconhecido: {modelo}")

# =======================================================================
# 🧩 SISTEMA DE MEMÓRIA SIMPLES (Session State)
# =======================================================================
class MemoriaConversa:
    def __init__(self):
        self.historico = []
    
    def adicionar_mensagem(self, role: str, content: str):
        self.historico.append({"role": role, "content": content})
    
    def obter_historico(self, limit=6):
        """Retorna as últimas mensagens (limit por role)"""
        return self.historico[-limit*2:]  # user + assistant
    
    def limpar(self):
        self.historico = []
    
    def contar_interacoes(self):
        return len([m for m in self.historico if m['role'] == 'user'])

# Memória global
memoria_simples = MemoriaConversa()

# =======================================================================
# 🧩 FUNÇÃO: Gerar resposta com memória simples
# =======================================================================
def gerar_resposta_com_memoria(pergunta: str, llm=None, usar_memoria=True):
    """
    Gera resposta usando sistema de memória simples e robusto.
    """
    if llm is None:
        llm = load_llm("Mistral")

    # Construir mensagens
    messages = []
    
    # Mensagem do sistema
    system_content = """És um tutor virtual educacional especializado em ajudar alunos. 
    Explica conceitos com clareza, dá exemplos e adapta o tom conforme a dificuldade. 
    
    Se houver histórico de conversa, usa-o para dar respostas contextuais e coerentes.
    Faz conexões com perguntas anteriores quando for relevante."""
    
    messages.append(SystemMessage(content=system_content))
    
    # Adicionar histórico se estiver usando memória
    if usar_memoria:
        historico = memoria_simples.obter_historico()
        for msg in historico:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
    
    # Adicionar pergunta atual
    messages.append(HumanMessage(content=pergunta))

    # Criar prompt e gerar resposta
    try:
        prompt = ChatPromptTemplate.from_messages(messages)
        resposta = llm.invoke(prompt.format_messages())
        resposta_texto = resposta.content.strip()
        
        # Salvar na memória se estiver usando memória
        if usar_memoria:
            memoria_simples.adicionar_mensagem('user', pergunta)
            memoria_simples.adicionar_mensagem('assistant', resposta_texto)
        
        return resposta_texto
        
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

# =======================================================================
# 🧩 FUNÇÃO: Gerar resposta simples (para compatibilidade)
# =======================================================================
def gerar_resposta(pergunta: str, llm=None):
    """
    Função original mantida para compatibilidade.
    """
    return gerar_resposta_com_memoria(pergunta, llm, usar_memoria=False)

# =======================================================================
# 🔧 FUNÇÕES DE GERENCIAMENTO DE MEMÓRIA
# =======================================================================
def limpar_memoria():
    """Limpa toda a memória da conversa"""
    memoria_simples.limpar()
    return "Memória limpa com sucesso!"

def obter_tamanho_memoria():
    """Retorna quantas interações estão na memória"""
    return memoria_simples.contar_interacoes()

def obter_historico_memoria():
    """Retorna o histórico atual da memória"""
    return memoria_simples.historico