from langchain.document_loaders import TextLoader  # Cambio clave
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def process_documents():
    # Cargar desde .txt
    loaders = [TextLoader(f"/app/rag/data/{name}.txt") for name in ["persona1", "persona2"]]

    
    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    
    # Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " "]  # Priorizar saltos de línea
    )
    
    chunks = text_splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vector_db = FAISS.from_documents(chunks, embeddings)
    vector_db.save_local("rag_db")
    return vector_db


def load_vector_db():
    print("hola soy el load")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.load_local("/app/rag_db", embeddings, allow_dangerous_deserialization=True)