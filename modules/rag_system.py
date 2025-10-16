# modules/rag_system.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Caminhos das pastas de dados
DOCS_PATH = "data/docs/"
DB_PATH = "data/chroma_db/"

def criar_base_conhecimento(pdf_path: str):
    """
    Cria uma base de conhecimento a partir de um documento PDF.
    """
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Dividir o texto em partes menores
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    textos = splitter.split_documents(docs)

    # Gerar embeddings e armazenar no ChromaDB
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(textos, embeddings, persist_directory=DB_PATH)
    db.persist()
    return db


def carregar_base_conhecimento():
    """
    Carrega a base de conhecimento vetorial persistida no diretório.
    """
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=DB_PATH, embedding_function=embeddings)


# Inicializar o sistema RAG
db = carregar_base_conhecimento()
retriever = db.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

