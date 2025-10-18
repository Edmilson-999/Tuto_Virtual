# app.py
import streamlit as st
import os

# Importações dos módulos internos
from modules.chatbot import gerar_resposta, load_llm
from modules.rag_system import qa_chain, criar_base_conhecimento
from utils.helpers import listar_pdfs

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="Tutor Virtual Inteligente", page_icon="🤖")

st.title("🎓 Tutor Virtual Inteligente com IA e RAG")
st.write("""
Bem-vindo! Este tutor combina **IA conversacional** com **busca em documentos (RAG)** 
para responder às suas perguntas de forma personalizada e contextualizada.
""")

# ---------------- BASE DE CONHECIMENTO ----------------
st.sidebar.header("📚 Base de Conhecimento")

pdfs = listar_pdfs()

if not pdfs:
    st.sidebar.warning("⚠️ Nenhum documento encontrado em `data/docs/`.")
    st.sidebar.info("Adicione arquivos PDF na pasta `data/docs/` para o tutor poder estudar.")
else:
    st.sidebar.success(f"{len(pdfs)} documento(s) disponível(is).")
    st.sidebar.write(pdfs)

# Botão para atualizar base
if st.sidebar.button("🔄 Atualizar base de conhecimento"):
    with st.spinner("A processar documentos..."):
        for pdf in pdfs:
            caminho = os.path.join("data/docs", pdf)
            criar_base_conhecimento(caminho)
        st.sidebar.success("✅ Base de conhecimento atualizada com sucesso!")

st.sidebar.markdown("---")
st.sidebar.info("💬 Use o campo abaixo para conversar com o tutor.")

# ---------------- INTERFACE DE CHAT ----------------
st.subheader("💬 Faça uma pergunta")

pergunta = st.text_input("Digite sua pergunta aqui:")
modo = st.radio(
    "Escolha o modo de resposta:",
    ["Com base nos PDFs (RAG)", "Somente Chatbot Base"],
    index=0
)

# Opção para alternar entre modelos
modelo_escolhido = st.selectbox(
    "🧠 Escolha o modelo de IA:",
    ["Mistral", "OpenAI GPT-4"],
    index=0
)

# ---------------- PROCESSAMENTO ----------------
if pergunta:
    with st.spinner("A pensar... 🤔"):
        try:
            if modo == "Com base nos PDFs (RAG)":
                resposta = qa_chain.invoke({"query": pergunta})
                st.markdown(f"**🤖 Tutor:** {resposta['result']}")
            else:
                # Carregar modelo escolhido dinamicamente
                llm = load_llm(modelo=modelo_escolhido)
                resposta = gerar_resposta(pergunta, llm)
                st.markdown(f"**🤖 Tutor:** {resposta}")
        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {e}")

# ---------------- RODAPÉ ----------------
st.markdown("---")
st.caption("Desenvolvido como parte do TCC — Tutor Virtual Inteligente com IA e Recomendação de Conteúdos 💡")
