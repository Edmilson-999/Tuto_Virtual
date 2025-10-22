"""
app.py
Tutor Virtual Inteligente - Versão Simplificada
"""

import streamlit as st
import os
from modules.chatbot import gerar_resposta, load_llm
from modules.rag_system import qa_chain, processar_todos_pdfs
from utils.helpers import listar_pdfs

# ================= CONFIGURAÇÃO =================
st.set_page_config(
    page_title="Tutor Virtual IA",
    page_icon="🤖",
    layout="centered"
)

# ================= CABEÇALHO SIMPLES =================
st.title("Tutor Virtual Inteligente")
st.write("Faça perguntas e receba respostas com base nos seus documentos PDF.")

# ================= SIDEBAR SIMPLIFICADA =================
with st.sidebar:
    st.header("📚 Documentos")
    
    pdfs = listar_pdfs()
    
    if not pdfs:
        st.warning("Adicione PDFs em `data/docs/`")
    else:
        st.success(f"{len(pdfs)} PDF(s) encontrado(s)")
        for pdf in pdfs:
            st.write(f"• {pdf}")
    
    # Processamento de PDFs
    if st.button("🔄 Processar PDFs", type="secondary"):
        if pdfs:
            with st.spinner("Processando..."):
                if processar_todos_pdfs():
                    st.success("PDFs processados!")
                    st.rerun()
                else:
                    st.error("Erro no processamento")
        else:
            st.warning("Nenhum PDF para processar")
    
    st.divider()
    
    # Configurações simples
    st.header("⚙️ Configurações")
    modelo = st.selectbox("Modelo IA:", ["Mistral", "OpenAI GPT-4"])
    
    # Verificar RAG
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
        ["Com base nos PDFs", "Chatbot básico"],
        horizontal=True
    )
else:
    modo = "Chatbot básico"
    st.info("💡 Adicione PDFs e processe para ativar o modo com documentos")

# Histórico do chat
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
                if modo == "Com base nos PDFs" and qa_chain:
                    resposta = qa_chain.invoke({"query": pergunta})
                    resposta_texto = resposta['result']
                else:
                    llm = load_llm(modelo=modelo)
                    resposta_texto = gerar_resposta(pergunta, llm)
                
                st.markdown(resposta_texto)
                st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                
            except Exception as e:
                erro = f"Erro: {str(e)}"
                st.error(erro)
                st.session_state.messages.append({"role": "assistant", "content": erro})

# ================= RODAPÉ SIMPLES =================
st.divider()
st.caption("Tutor Virtual • Desenvolvido com Streamlit e IA")