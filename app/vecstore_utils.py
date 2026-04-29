from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


# Create embeddings (HF - FREE)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


# Create FAISS vector DB
def create_vector_store(documents):
    embeddings = get_embeddings()
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db


# Retrieve relevant chunks
def retrieve_docs(vector_db, query, k=3):
    return vector_db.similarity_search(query, k=k)