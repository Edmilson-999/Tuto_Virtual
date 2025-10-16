# app.py
import streamlit as st
from modules.chatbot import gerar_resposta
from modules.rag_system import qa_chain, criar_base_conhecimento
from utils.helpers import listar_pdfs
import os

st.set_page_config(page_title="Tutor Virtual Inteligente", page_icon="🤖")

st.title("🎓 Tutor Virtual Inteligente com IA e RAG")
st.write("Bem-vindo! Este tutor usa **IA conversacional** e **busca em documentos** para responder às suas perguntas de forma personalizada.")

# --- Seção 1: Atualizar base de conhecimento ---
st.sidebar.header("📚 Base de Conhecimento")

# Listar PDFs existentes
pdfs = listar_pdfs()

if not pdfs:
    st.sidebar.warning("⚠️ Nenhum documento encontrado em `data/docs/`.")
    st.sidebar.info("Adicione arquivos PDF na pasta `data/docs/` para o tutor poder estudar.")
else:
    st.sidebar.success(f"{len(pdfs)} documento(s) disponível(is).")
    st.sidebar.write(pdfs)

# Botão para recarregar base de conhecimento
if st.sidebar.button("🔄 Atualizar base de conhecimento"):
    for pdf in pdfs:
        caminho = os.path.join("data/docs", pdf)
        criar_base_conhecimento(caminho)
    st.sidebar.success("✅ Base de conhecimento atualizada com sucesso!")

st.sidebar.markdown("---")
st.sidebar.info("Use o campo abaixo para conversar com o tutor.")

# --- Seção 2: Interação principal ---
st.subheader("💬 Faça uma pergunta")
pergunta = st.text_input("Digite sua pergunta aqui:")

modo = st.radio(
    "Escolha o modo de resposta:",
    ["Com base nos PDFs (RAG)", "Somente Chatbot Base"],
    index=0
)

if pergunta:
    with st.spinner("A pensar... 🤔"):
        try:
            if modo == "Com base nos PDFs (RAG)":
                resposta = qa_chain.invoke({"query": pergunta})
                st.markdown(f"**🤖 Tutor:** {resposta['result']}")
            else:
                resposta = gerar_resposta(pergunta)
                st.markdown(f"**🤖 Tutor:** {resposta}")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
