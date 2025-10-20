"""
modules/rag_system.py
Sistema RAG com correção de caminhos para Windows
"""

import os
import shutil
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suprimir warnings desnecessários
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

load_dotenv()

# Caminhos
DOCS_PATH = "data/docs/"
DB_PATH = "data/chroma_db/"

def carregar_embeddings_locais():
    """Carrega modelo de embeddings local"""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )
        
        print("✅ Embeddings locais carregados")
        return embeddings
        
    except Exception as e:
        print(f"❌ Erro ao carregar embeddings: {e}")
        raise

def criar_base_conhecimento(pdf_path: str):
    """Cria base de conhecimento a partir de PDF"""
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_chroma import Chroma
        
        # Verificar se arquivo existe
        if not os.path.exists(pdf_path):
            print(f"   ❌ Arquivo não encontrado: {pdf_path}")
            return None
            
        # Carregar PDF
        loader = PyPDFLoader(pdf_path)
        documentos = loader.load()
        
        if not documentos:
            print(f"   ⚠️ PDF vazio ou corrompido: {pdf_path}")
            return None

        # Dividir texto
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documentos)
        
        print(f"   📄 Criados {len(chunks)} chunks")

        # Embeddings locais
        embeddings = carregar_embeddings_locais()

        # Criar vector store
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=DB_PATH
        )
        
        print(f"   ✅ PDF processado com sucesso")
        return vector_store
        
    except Exception as e:
        print(f"   ❌ Erro ao processar PDF: {e}")
        return None

def carregar_base_conhecimento():
    """Carrega base existente"""
    try:
        from langchain_chroma import Chroma
        
        if not os.path.exists(DB_PATH) or not os.listdir(DB_PATH):
            return None

        embeddings = carregar_embeddings_locais()
        vector_store = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )
        
        # Testar se funciona
        count = vector_store._collection.count()
        print(f"✅ Base carregada com {count} documentos")
        return vector_store
        
    except Exception as e:
        print(f"❌ Erro ao carregar base: {e}")
        return None

def inicializar_sistema_rag():
    """Inicializa sistema RAG"""
    try:
        # Verificar API key do Mistral
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_key:
            print("⚠️ Mistral API key não configurada")
            return None, None

        # Carregar base
        vector_store = carregar_base_conhecimento()
        if not vector_store:
            print("ℹ️ Nenhuma base encontrada. Adicione PDFs primeiro.")
            return None, None

        # Configurar LLM
        from langchain_mistralai import ChatMistralAI
        llm = ChatMistralAI(
            model="mistral-small-latest",
            api_key=mistral_key,
            temperature=0.6
        )

        # Configurar retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        # Criar QA chain
        from langchain.chains import RetrievalQA
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        print("🚀 Sistema RAG inicializado com sucesso")
        return qa_chain, vector_store
        
    except Exception as e:
        print(f"❌ Erro ao inicializar RAG: {e}")
        return None, None

def processar_todos_pdfs():
    """Processa todos os PDFs com caminhos corrigidos"""
    try:
        from utils.helpers import listar_pdfs, get_caminho_pdf, verificar_pdf_valido
        
        pdfs = listar_pdfs()
        if not pdfs:
            print("📭 Nenhum PDF encontrado em data/docs/")
            return False

        print(f"📚 Encontrados {len(pdfs)} PDFs para processar")
        
        # Limpar base anterior
        if os.path.exists(DB_PATH):
            shutil.rmtree(DB_PATH)
            print("🧹 Base anterior removida")

        success_count = 0
        for pdf_nome in pdfs:
            try:
                # Obter caminho correto
                pdf_path = get_caminho_pdf(pdf_nome)
                
                print(f"📘 Processando: {pdf_nome}")
                
                # Verificar se o arquivo existe
                if not verificar_pdf_valido(pdf_path):
                    print(f"   ❌ Arquivo inválido: {pdf_path}")
                    continue
                
                # Processar PDF
                if criar_base_conhecimento(pdf_path):
                    success_count += 1
                    print(f"   ✅ Sucesso")
                else:
                    print(f"   ❌ Falha")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                continue

        if success_count > 0:
            print(f"🎉 {success_count}/{len(pdfs)} PDFs processados com sucesso!")
            
            # Recarregar sistema RAG
            global qa_chain, vector_store
            qa_chain, vector_store = inicializar_sistema_rag()
            
            return True
        else:
            print("❌ Nenhum PDF pôde ser processado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return False

def limpar_base_conhecimento():
    """Limpa a base de dados"""
    try:
        if os.path.exists(DB_PATH):
            shutil.rmtree(DB_PATH)
            print("🧹 Base de conhecimento limpa")
            return True
        return False
    except Exception as e:
        print(f"❌ Erro ao limpar base: {e}")
        return False

# Inicialização
qa_chain, vector_store = inicializar_sistema_rag()

# Teste
if __name__ == "__main__":
    print("🧪 Testando sistema RAG...")
    
    # Testar se PDFs estão acessíveis
    from utils.helpers import listar_pdfs, get_caminho_pdf
    
    pdfs = listar_pdfs()
    print(f"📁 PDFs encontrados: {len(pdfs)}")
    
    for pdf in pdfs:
        caminho = get_caminho_pdf(pdf)
        existe = os.path.exists(caminho)
        print(f"   {pdf}: {'✅' if existe else '❌'} {caminho}")
    
    # Testar embeddings
    try:
        embeddings = carregar_embeddings_locais()
        test_vector = embeddings.embed_query("teste")
        print(f"✅ Embeddings: {len(test_vector)} dimensões")
    except Exception as e:
        print(f"❌ Erro nos embeddings: {e}")
    
    # Testar base
    base = carregar_base_conhecimento()
    if base:
        print("✅ Base carregada - sistema pronto!")
    else:
        print("ℹ️ Execute o processamento de PDFs primeiro")