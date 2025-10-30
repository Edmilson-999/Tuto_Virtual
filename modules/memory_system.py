"""
modules/memory_system.py
Sistema de memória simplificado e corrigido
"""

from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import BaseMessage
from typing import List, Dict, Any

class SistemaMemoria:
    def __init__(self, window_size=6):
        """
        Inicializa o sistema de memória simplificado.
        """
        self.memory = ConversationBufferWindowMemory(
            k=window_size,
            return_messages=True,
            memory_key="chat_history"
        )
    
    def adicionar_interacao(self, pergunta: str, resposta: str):
        """
        Adiciona uma interação à memória.
        """
        self.memory.save_context(
            {"input": pergunta},
            {"output": resposta}
        )
    
    def obter_historico(self) -> List[Dict[str, Any]]:
        """
        Retorna o histórico formatado para o prompt.
        """
        try:
            historico = self.memory.load_memory_variables({})
            return historico.get("chat_history", [])
        except Exception as e:
            print(f"Erro ao carregar histórico: {e}")
            return []
    
    def limpar_memoria(self):
        """
        Limpa toda a memória da conversa.
        """
        self.memory.clear()
    
    def obter_historico_simples(self) -> List[Dict[str, str]]:
        """
        Retorna o histórico em formato simples para a interface.
        """
        try:
            messages = self.obter_historico()
            historico_simples = []
            
            for msg in messages:
                if hasattr(msg, 'type'):
                    if msg.type == 'human':
                        historico_simples.append({'role': 'user', 'content': msg.content})
                    elif msg.type == 'ai':
                        historico_simples.append({'role': 'assistant', 'content': msg.content})
                elif hasattr(msg, 'get'):
                    # Fallback para diferentes formatos
                    content = msg.get('content', '') if hasattr(msg, 'get') else str(msg)
                    role = 'user' if 'input' in str(msg).lower() else 'assistant'
                    historico_simples.append({'role': role, 'content': content})
            
            return historico_simples
        except Exception as e:
            print(f"Erro ao converter histórico: {e}")
            return []

# Instância global do sistema de memória
memoria_global = SistemaMemoria(window_size=6)