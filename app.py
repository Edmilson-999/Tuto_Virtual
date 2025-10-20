# app.py (parte atualizada)
import streamlit as st
import os

# Importações dos módulos internos
from modules.chatbot import gerar_resposta, load_llm
from modules.rag_system import processar_todos_pdfs, qa_chain, criar_base_conhecimento, inicializar_sistema_rag
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

if not pdfs:"""
app.py
Interface principal do Tutor Virtual Inteligente
Versão compatível com embeddings locais e tratamento de erros melhorado
"""

import streamlit as st
import os
import sys

# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações dos módulos internos
from modules.chatbot import gerar_resposta, load_llm
from modules.rag_system import qa_chain, criar_base_conhecimento, processar_todos_pdfs, carregar_base_conhecimento
from utils.helpers import listar_pdfs

# ---------------- CONFIGURAÇÃO INICIAL ----------------
st.set_page_config(
    page_title="Tutor Virtual Inteligente", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ESTILOS CSS PERSONALIZADOS ----------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e6f3ff;
        border-left: 4px solid #1f77b4;
    }
    .bot-message {
        background-color: #f0f8ff;
        border-left: 4px solid #ff6b6b;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO PRINCIPAL ----------------
st.markdown('<div class="main-header">🎓 Tutor Virtual Inteligente</div>', unsafe_allow_html=True)
st.markdown("""
<div class="sub-header">
    Combina <strong>IA conversacional</strong> com <strong>busca em documentos (RAG)</strong> 
    para responder às suas perguntas de forma personalizada e contextualizada.
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR: CONFIGURAÇÕES E BASE DE CONHECIMENTO ----------------
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Seção de Modelo de IA
    st.subheader("🧠 Modelo de IA")
    modelo_escolhido = st.selectbox(
        "Escolha o modelo:",
        ["Mistral", "OpenAI GPT-4"],
        index=0,
        help="Mistral é recomendado para melhor custo-benefício"
    )
    
    # Verificar se as API keys estão configuradas
    st.subheader("🔑 Status das APIs")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    mistral_key = os.getenv("MISTRAL_API_KEY")
    
    if openai_key:
        st.success("✅ OpenAI API Key configurada")
    else:
        st.error("❌ OpenAI API Key não encontrada")
        
    if mistral_key:
        st.success("✅ Mistral API Key configurada")
    else:
        st.error("❌ Mistral API Key não encontrada")
    
    # Seção de Base de Conhecimento
    st.header("📚 Base de Conhecimento")
    
    # Listar PDFs disponíveis
    pdfs = listar_pdfs()
    
    if not pdfs:
        st.warning("""
        ⚠️ Nenhum documento PDF encontrado.
        
        Para usar o sistema RAG, adicione arquivos PDF na pasta `data/docs/`.
        """)
    else:
        st.success(f"📖 {len(pdfs)} documento(s) disponível(is):")
        for pdf in pdfs:
            st.write(f"• {pdf}")
    
    # Botões de gerenciamento da base de conhecimento
    st.subheader("🛠️ Gerenciamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Processar PDFs", help="Processa todos os PDFs com embeddings locais"):
            if not pdfs:
                st.error("❌ Nenhum PDF para processar")
            else:
                with st.spinner("Processando documentos com IA local..."):
                    try:
                        success = processar_todos_pdfs()
                        if success:
                            st.success("✅ Base criada com embeddings locais!")
                            # Recarregar a página para atualizar o estado
                            st.rerun()
                        else:
                            st.error("❌ Falha ao processar PDFs. Verifique os logs.")
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
    
    with col2:
        if st.button("🧹 Limpar Base", help="Limpa toda a base de conhecimento"):
            try:
                from modules.rag_system import limpar_base_conhecimento
                if limpar_base_conhecimento():
                    st.success("✅ Base limpa com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao limpar base")
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    
    # Informações do sistema
    st.markdown("---")
    st.header("ℹ️ Informações")
    
    # Verificar status do RAG
    if qa_chain is not None:
        st.success("✅ Sistema RAG Ativo")
        st.caption("O tutor pode responder com base nos seus documentos")
    else:
        st.warning("⚠️ Sistema RAG Inativo")
        st.caption("Adicione PDFs e processe para ativar o RAG")
    
    st.info("""
    **Modo de Uso:**
    - **Com RAG**: Respostas baseadas nos seus documentos
    - **Sem RAG**: Respostas gerais do modelo de IA
    """)

# ---------------- ÁREA PRINCIPAL: CHAT INTERATIVO ----------------
st.header("💬 Chat com o Tutor")

# Inicializar histórico de chat na session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Verificar disponibilidade do RAG
rag_disponivel = qa_chain is not None and pdfs

# Seletor de modo de resposta
if rag_disponivel:
    modo = st.radio(
        "**Modo de Resposta:**",
        ["Com base nos PDFs (RAG)", "Somente Chatbot Base"],
        index=0,
        horizontal=True
    )
    st.caption("🎯 **RAG**: Respostas contextuais dos seus documentos | **Base**: Respostas gerais da IA")
else:
    modo = "Somente Chatbot Base"
    st.warning("""
    🔄 **Sistema RAG Indisponível** 
    - Adicione PDFs na pasta `data/docs/` 
    - Clique em 'Processar PDFs' na sidebar
    - Atualmente usando modo chatbot básico
    """)

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Mostrar fontes se disponível no modo RAG
        if message.get("sources") and modo == "Com base nos PDFs (RAG)":
            with st.expander("📚 Fontes utilizadas"):
                for i, source in enumerate(message["sources"][:2]):
                    st.write(f"**Fonte {i+1}:** {source}")

# Input de pergunta do usuário
pergunta = st.chat_input("Digite sua pergunta aqui...")

# ---------------- PROCESSAMENTO DA PERGUNTA ----------------
if pergunta:
    # Adicionar pergunta do usuário ao chat
    st.session_state.messages.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Gerar resposta com spinner
    with st.chat_message("assistant"):
        with st.spinner("🤔 Tutor está pensando..."):
            try:
                if modo == "Com base nos PDFs (RAG)" and rag_disponivel:
                    # Modo RAG - usar base de conhecimento
                    resposta_completa = qa_chain.invoke({"query": pergunta})
                    resposta_texto = resposta_completa['result']
                    
                    # Extrair fontes se disponíveis
                    fontes = []
                    if 'source_documents' in resposta_completa:
                        for doc in resposta_completa['source_documents']:
                            fonte = doc.metadata.get('source', 'Documento')
                            if fonte not in fontes:
                                fontes.append(fonte)
                    
                    # Exibir resposta
                    st.markdown(resposta_texto)
                    
                    # Exibir fontes se disponíveis
                    if fontes:
                        with st.expander("📚 Ver fontes utilizadas"):
                            for i, fonte in enumerate(fontes):
                                nome_arquivo = os.path.basename(fonte)
                                st.write(f"• {nome_arquivo}")
                    
                    # Salvar no histórico com fontes
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": resposta_texto,
                        "sources": fontes
                    })
                    
                else:
                    # Modo Chatbot Base - apenas LLM
                    llm = load_llm(modelo=modelo_escolhido)
                    resposta_texto = gerar_resposta(pergunta, llm)
                    st.markdown(resposta_texto)
                    
                    # Salvar no histórico
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": resposta_texto
                    })
                    
            except Exception as e:
                erro_msg = f"""
                ❌ **Ocorreu um erro ao processar sua pergunta:**
                
                `{str(e)}`
                
                **Sugestões:**
                - Verifique sua conexão com a internet
                - Tente usar o modo "Somente Chatbot Base"
                - Verifique se as API keys estão configuradas corretamente
                - Recarregue a página e tente novamente
                """
                st.error(erro_msg)
                
                # Salvar mensagem de erro no histórico
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Erro: {str(e)}"
                })

# ---------------- SEÇÃO DE RECOMENDAÇÕES (FUTURO) ----------------
st.markdown("---")
st.header("🎯 Recomendações de Conteúdo")

# Placeholder para o sistema de recomendações
st.info("""
**🚧 Sistema de Recomendações em Desenvolvimento**

Em breve, o tutor irá:
- 📊 Analisar seu padrão de perguntas
- 📚 Recomendar conteúdos personalizados
- 🎯 Sugerir tópicos para estudo baseado nas suas dificuldades
- 📈 Acompanhar seu progresso de aprendizado
""")

# Exemplo de recomendações estáticas (para demonstração)
if st.session_state.messages:
    st.subheader("💡 Sugestões Baseadas na Conversa")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Perguntas Realizadas", len([m for m in st.session_state.messages if m["role"] == "user"]))
    
    with col2:
        st.metric("Respostas Geradas", len([m for m in st.session_state.messages if m["role"] == "assistant"]))
    
    with col3:
        if rag_disponivel:
            st.metric("Documentos na Base", len(pdfs))
        else:
            st.metric("Modo", "Chat Básico")

# -sidebar: CONTROLES ADICIONAIS ----------------
with st.sidebar:
    st.markdown("---")
    st.header("🔧 Utilitários")
    
    # Botão para limpar histórico
    if st.button("🗑️ Limpar Histórico", help="Limpa todo o histórico de conversa"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.success("Histórico limpo!")
        st.rerun()
    
    # Botão para debug (apenas desenvolvimento)
    if st.checkbox("🐛 Modo Debug", help="Mostra informações técnicas"):
        st.subheader("Informações de Debug")
        st.json({
            "total_mensagens": len(st.session_state.messages),
            "rag_disponivel": rag_disponivel,
            "pdfs_encontrados": len(pdfs),
            "modelo_selecionado": modelo_escolhido,
            "modo_atual": modo
        })

# ---------------- RODAPÉ ----------------
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

with footer_col1:
    st.caption("""
    **Desenvolvido como parte do TCC — Tutor Virtual Inteligente com IA e Recomendação de Conteúdos** 💡
    
    *Tecnologias: Streamlit • LangChain • ChromaDB • Mistral AI • Sentence Transformers*
    """)

with footer_col2:
    st.caption("""
    **Status:**
    - 🤖 Chat: ✅ Ativo
    - 📚 RAG: {} 
    - 🎯 Recomendações: 🚧 Desenvolvimento
    """.format("✅ Ativo" if rag_disponivel else "❌ Inativo"))

with footer_col3:
    st.caption("""
    **Ajuda:**
    - 💬 Faça perguntas específicas
    - 📁 Adicione PDFs para contexto
    - 🔄 Processe os documentos
    - 🎯 Use o modo RAG para respostas precisas
    """)

# ---------------- FUNÇÕES AUXILIARES ----------------
def verificar_dependencias():
    """
    Verifica se todas as dependências estão disponíveis
    """
    try:
        from modules.rag_system import carregar_embeddings_locais
        embeddings = carregar_embeddings_locais()
        return True, "✅ Todas as dependências estão OK"
    except Exception as e:
        return False, f"❌ Erro nas dependências: {e}"

# Verificação automática ao carregar (apenas no primeiro carregamento)
if "deps_checked" not in st.session_state:
    st.session_state.deps_checked = True
    status, mensagem = verificar_dependencias()
    
    if not status:
        st.sidebar.error(mensagem)
    else:
        st.sidebar.success("Sistema verificado e pronto!")
    st.sidebar.warning("⚠️ Nenhum documento encontrado em `data/docs/`.")
    st.sidebar.info("Adicione arquivos PDF na pasta `data/docs/` para o tutor poder estudar.")
else:
    st.sidebar.success(f"{len(pdfs)} documento(s) disponível(is).")
    for pdf in pdfs:
        st.sidebar.write(f"• {pdf}")

# Botão para atualizar base
# No app.py, procure esta seção e atualize:
if st.sidebar.button("🔄 Atualizar base de conhecimento"):
    with st.spinner("Processando documentos com IA local..."):
        try:
            success = processar_todos_pdfs()
            if success:
                st.sidebar.success("✅ Base criada com embeddings locais!")
            else:
                st.sidebar.error("❌ Falha ao processar PDFs")
        except Exception as e:
            st.sidebar.error(f"❌ Erro: {e}")

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