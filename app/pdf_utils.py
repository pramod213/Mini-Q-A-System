# from langchain_community.document_loaders import PyPDFLoader

# def load_pdf(file_path: str):
#     """
#     Load PDF and return LangChain documents
#     """
#     loader = PyPDFLoader(file_path)
#     documents = loader.load()
#     return documents










from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# -----------------------------
# TEXT SPLITTING
# -----------------------------
def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    return [Document(page_content=chunk) for chunk in chunks]


# -----------------------------
# LOAD + SPLIT PDF TEXT
# (expects raw extracted text)
# -----------------------------
def load_and_split_pdf(text: str):
    return split_text(text)