"""
modules/rag_system.py
Módulo responsável por criar e carregar a base de conhecimento (RAG)
usando PDFs e embeddings vetoriais com ChromaDB.
Versão corrigida com imports compatíveis.
"""

import os
from shutil import rmtree
from dotenv import load_dotenv

# Importações compatíveis
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_mistralai import ChatMistralAI

# Importação alternativa para RetrievalQA baseada na versão
try:
    # Para versões mais recentes do LangChain
    from langchain.chains import RetrievalQA
except ImportError:
    # Fallback para versões mais antigas
    from langchain.chains.retrieval_qa.base import RetrievalQA

# Carrega variáveis do .env
load_dotenv()

# Caminhos
DOCS_PATH = "data/docs/"
DB_PATH = "data/chroma_db/"

# ===================================================================
# 🧠 Função: Criar base de conhecimento a partir de PDFs
# ===================================================================
def criar_base_conhecimento(pdf_path: str):
    """
    Cria ou atualiza a base de conhecimento vetorial a partir de um PDF.
    Divide o texto, gera embeddings e salva localmente no ChromaDB.
    """
    print(f"📘 Processando documento: {pdf_path}")
    
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        # Dividir texto em blocos menores
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        textos = splitter.split_documents(docs)

        # Gerar embeddings com OpenAI
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

        # Criar ou atualizar o banco vetorial
        db = Chroma.from_documents(
            documents=textos, 
            embedding=embeddings, 
            persist_directory=DB_PATH
        )
        
        print("✅ Base de conhecimento atualizada com sucesso.")
        return db
        
    except Exception as e:
        print(f"❌ Erro ao processar documento {pdf_path}: {e}")
        raise

# ===================================================================
# 💾 Função: Carregar base de conhecimento existente
# ===================================================================
def carregar_base_conhecimento():
    """
    Carrega a base de conhecimento persistida em DB_PATH.
    Versão corrigida para evitar erros de compatibilidade.
    """
    try:
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        
        if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
            # Tenta carregar base existente
            try:
                db = Chroma(
                    persist_directory=DB_PATH, 
                    embedding_function=embeddings
                )
                print("✅ Base de conhecimento carregada com sucesso.")
                return db
            except Exception as e:
                print(f"⚠️ Erro ao carregar base existente: {e}")
                print("🧹 Recriando base de conhecimento...")
                # Limpa o diretório e cria novo
                try:
                    rmtree(DB_PATH)
                except:
                    pass
                
        # Se não existir ou falhar ao carregar, cria diretório
        os.makedirs(DB_PATH, exist_ok=True)
        
        # Cria uma nova base vazia
        db = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )
        return db
        
    except Exception as e:
        print(f"❌ Erro crítico ao carregar base: {e}")
        raise

# ===================================================================
# 🔗 Inicialização segura do sistema RAG
# ===================================================================
def inicializar_sistema_rag():
    """
    Inicializa o sistema RAG de forma segura, tratando possíveis erros.
    """
    try:
        # Verificar se as API keys estão disponíveis
        openai_key = os.getenv("OPENAI_API_KEY")
        mistral_key = os.getenv("MISTRAL_API_KEY")
        
        if not openai_key or not mistral_key:
            print("⚠️ API keys não encontradas. Sistema RAG desativado.")
            return None, None

        # Carregar base de conhecimento
        db = carregar_base_conhecimento()
        
        # Configurar retriever
        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        # Modelo Mistral
        llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=mistral_key,
            temperature=0.6
        )

        # Criar cadeia de perguntas e respostas
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            verbose=False
        )
        
        return qa_chain, db
        
    except Exception as e:
        print(f"❌ Erro ao inicializar sistema RAG: {e}")
        return None, None

# Inicialização condicional
try:
    qa_chain, db = inicializar_sistema_rag()
    if qa_chain is None:
        print("⚠️ Sistema RAG não foi inicializado. Verifique as API keys e dependências.")
except Exception as e:
    print(f"⚠️ Falha na inicialização do RAG: {e}")
    qa_chain, db = None, None