# app.py (parte atualizada)
import streamlit as st
import os

# Importações dos módulos internos
from modules.chatbot import gerar_resposta, load_llm
from modules.rag_system import qa_chain, criar_base_conhecimento, inicializar_sistema_rag
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
    for pdf in pdfs:
        st.sidebar.write(f"• {pdf}")

# Botão para atualizar base
if st.sidebar.button("🔄 Atualizar base de conhecimento"):
    if not pdfs:
        st.sidebar.error("❌ Nenhum PDF encontrado para processar.")
    else:
        with st.spinner("A processar documentos..."):
            try:
                for pdf in pdfs:
                    caminho = os.path.join("data/docs", pdf)
                    criar_base_conhecimento(caminho)
                # Reinicializar o sistema RAG após atualização
               # global qa_chain
                qa_chain, _ = inicializar_sistema_rag()
                st.sidebar.success("✅ Base de conhecimento atualizada com sucesso!")
            except Exception as e:
                st.sidebar.error(f"❌ Erro ao processar documentos: {e}")

st.sidebar.markdown("---")
st.sidebar.info("💬 Use o campo abaixo para conversar com o tutor.")

# ---------------- INTERFACE DE CHAT ----------------
st.subheader("💬 Faça uma pergunta")

pergunta = st.text_input("Digite sua pergunta aqui:")

# Verificar se o sistema RAG está disponível
rag_disponivel = qa_chain is not None and pdfs

if rag_disponivel:
    modo = st.radio(
        "Escolha o modo de resposta:",
        ["Com base nos PDFs (RAG)", "Somente Chatbot Base"],
        index=0
    )
else:
    st.info("ℹ️ Modo RAG indisponível. Verifique se há PDFs na pasta `data/docs/` e se as API keys estão configuradas.")
    modo = "Somente Chatbot Base"

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
            if modo == "Com base nos PDFs (RAG)" and rag_disponivel:
                resposta = qa_chain.invoke({"query": pergunta})
                st.markdown(f"**🤖 Tutor (com RAG):** {resposta['result']}")
                
                # Mostrar fontes (opcional)
                with st.expander("📚 Ver fontes utilizadas"):
                    for i, doc in enumerate(resposta.get('source_documents', [])[:2]):
                        st.write(f"Fonte {i+1}: {doc.metadata.get('source', 'Desconhecida')}")
                        st.caption(doc.page_content[:200] + "...")
            else:
                # Carregar modelo escolhido dinamicamente
                llm = load_llm(modelo=modelo_escolhido)
                resposta = gerar_resposta(pergunta, llm)
                st.markdown(f"**🤖 Tutor:** {resposta}")
                
        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {e}")
            st.info("💡 Tente usar o modo 'Somente Chatbot Base' ou verifique a conexão com a API.")

# ---------------- RODAPÉ ----------------
st.markdown("---")
st.caption("Desenvolvido como parte do TCC — Tutor Virtual Inteligente com IA e Recomendação de Conteúdos 💡")