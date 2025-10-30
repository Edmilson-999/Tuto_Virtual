"""
app.py
Tutor Virtual com Sistema de Memória Corrigido
"""

import streamlit as st
import os
from modules.chatbot import (
    gerar_resposta_com_memoria, 
    load_llm, 
    limpar_memoria,
    obter_tamanho_memoria
)
from modules.rag_system import qa_chain, processar_todos_pdfs
from utils.helpers import listar_pdfs

# ================= CONFIGURAÇÃO =================
st.set_page_config(
    page_title="Tutor Virtual IA",
    page_icon="🤖",
    layout="centered"
)

# ================= CABEÇALHO =================
st.title("🎓 Tutor Virtual Inteligente")
st.write("Faça perguntas e receba respostas contextuais com memória de conversa.")

# ================= SIDEBAR =================
with st.sidebar:
    st.header("📚 Documentos")
    
    pdfs = listar_pdfs()
    
    if not pdfs:
        st.warning("Adicione PDFs em `data/docs/`")
    else:
        st.success(f"{len(pdfs)} PDF(s) encontrado(s)")
        for pdf in pdfs:
            st.write(f"• {pdf}")
    
    if st.button("🔄 Processar PDFs", type="secondary"):
        if pdfs:
            with st.spinner("Processando..."):
                if processar_todos_pdfs():
                    st.success("PDFs processados!")
                    st.rerun()
                else:
                    st.error("Erro no processamento")
    
    st.divider()
    
    # Configurações
    st.header("⚙️ Configurações")
    modelo = st.selectbox("Modelo IA:", ["Mistral", "OpenAI GPT-4"])
    
    # Controles de memória
    st.subheader("🧠 Memória")
    st.info(f"Interações na memória: {obter_tamanho_memoria()}")
    
    if st.button("🧹 Limpar Memória", type="secondary"):
        limpar_memoria()
        st.success("Memória limpa!")
        st.rerun()
    
    # Status RAG
    if qa_chain and pdfs:
        st.success("✅ RAG Ativo")
    else:
        st.warning("⚠️ RAG Inativo")

# ================= CHAT PRINCIPAL =================
st.divider()

# Seleção de modo
if qa_chain and pdfs:
    modo = st.radio(
        "**Modo de resposta:**",
        ["Com base nos PDFs", "Chatbot com memória", "Chatbot básico"],
        index=1,  # Default para memória
        horizontal=True
    )
else:
    modo = st.radio(
        "**Modo de resposta:**",
        ["Chatbot com memória", "Chatbot básico"],
        index=0,
        horizontal=True
    )

# Inicializar histórico na session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if pergunta := st.chat_input("Digite sua pergunta..."):
    # Adicionar pergunta ao histórico
    st.session_state.messages.append({"role": "user", "content": pergunta})
    
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Gerar resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                llm = load_llm(modelo=modelo)
                
                if modo == "Com base nos PDFs":
                    resposta = qa_chain.invoke({"query": pergunta})
                    resposta_texto = resposta['result']
                    
                elif modo == "Chatbot com memória":
                    resposta_texto = gerar_resposta_com_memoria(pergunta, llm, usar_memoria=True)
                    
                else:  # Chatbot básico
                    resposta_texto = gerar_resposta_com_memoria(pergunta, llm, usar_memoria=False)
                
                st.markdown(resposta_texto)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": resposta_texto
                })
                
            except Exception as e:
                erro = f"Erro: {str(e)}"
                st.error(erro)
                st.session_state.messages.append({"role": "assistant", "content": erro})

# ================= EXEMPLOS DE USO =================
st.divider()
st.write("💡 **Teste a memória:** Faça perguntas sequenciais como 'O que é Python?' depois 'E Java?'")

# ================= RODAPÉ =================
st.divider()
st.caption("Tutor Virtual • Com sistema de memória • Desenvolvido com Streamlit e IA")