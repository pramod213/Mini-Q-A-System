# # import re
# # from typing import List, Any


# # class RAGPipeline:
# #     """
# #     Simple, stable RAG wrapper around a VectorStoreRetriever.
# #     Fixes:
# #     - No .ask() error
# #     - LangChain version compatibility issues
# #     - Safe fallback for retrieval + formatting
# #     """

# #     def __init__(self, retriever: Any):
# #         """
# #         retriever: VectorStoreRetriever (FAISS, Chroma, etc.)
# #         """
# #         self.retriever = retriever

# #     # -----------------------------
# #     # MAIN PUBLIC METHOD (FIXED)
# #     # -----------------------------
# #     def ask(self, query: str) -> str:
# #         """
# #         Main function used in Streamlit:
# #         rag.ask("question")
# #         """

# #         docs = self._retrieve(query)
# #         return self._format_docs(docs)

# #     # -----------------------------
# #     # SAFE RETRIEVAL METHOD
# #     # -----------------------------
# #     def _retrieve(self, query: str) -> List[Any]:
# #         """
# #         Handles different LangChain versions safely.
# #         """

# #         if not isinstance(query, str):
# #             query = str(query)

# #         # New LangChain (preferred)
# #         if hasattr(self.retriever, "invoke"):
# #             return self.retriever.invoke(query)

# #         # Older LangChain
# #         if hasattr(self.retriever, "get_relevant_documents"):
# #             return self.retriever.get_relevant_documents(query)

# #         # Fallback (very old/custom retrievers)
# #         if hasattr(self.retriever, "retrieve"):
# #             return self.retriever.retrieve(query)

# #         raise AttributeError(
# #             "Unsupported retriever type: no valid retrieval method found."
# #         )

# #     # -----------------------------
# #     # FORMAT OUTPUT CLEANLY
# #     # -----------------------------
# #     def _format_docs(self, docs: List[Any]) -> str:
# #         """
# #         Converts retrieved docs into readable answer text.
# #         """

# #         if not docs:
# #             return "❌ No relevant information found."

# #         texts = []

# #         for d in docs:
# #             # LangChain Document object support
# #             if hasattr(d, "page_content"):
# #                 texts.append(d.page_content)

# #             # dict support (some vector DBs return dicts)
# #             elif isinstance(d, dict) and "page_content" in d:
# #                 texts.append(d["page_content"])

# #             # raw string fallback
# #             else:
# #                 texts.append(str(d))

# #         # clean duplicates & empty lines
# #         cleaned = self._clean_text("\n\n".join(texts))

# #         return cleaned

# #     # -----------------------------
# #     # TEXT CLEANING UTILITY
# #     # -----------------------------
# #     def _clean_text(self, text: str) -> str:
# #         """
# #         Removes excessive whitespace and improves readability.
# #         """

# #         text = re.sub(r"\n{3,}", "\n\n", text)
# #         text = re.sub(r"[ \t]+", " ", text)

# #         return text.strip()








# # -------------------------------------------------------------------------------------------








# # from typing import List, Tuple, Any

# # from langchain_core.documents import Document
# # from langchain_text_splitters import RecursiveCharacterTextSplitter

# # from langchain_community.vectorstores import FAISS
# # from langchain_huggingface import HuggingFaceEmbeddings


# # # ==============================
# # # CONFIG
# # # ==============================

# # CHUNK_SIZE = 400
# # CHUNK_OVERLAP = 100
# # TOP_K = 4

# # EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# # # ==============================
# # # INPUT VALIDATION + NORMALIZATION
# # # ==============================

# # def normalize_input(data: Any) -> List[Document]:
# #     """
# #     Converts input into List[Document]
# #     Supports:
# #     - str
# #     - list[str]
# #     - list[Document]
# #     """

# #     if data is None:
# #         raise ValueError("❌ Input is None. No document received.")

# #     # bytes (common PDF bug case)
# #     if isinstance(data, bytes):
# #         data = data.decode("utf-8", errors="ignore")

# #     # single string
# #     if isinstance(data, str):
# #         data = data.strip()
# #         if not data:
# #             raise ValueError("❌ Empty text provided.")
# #         return [Document(page_content=data)]

# #     # list of strings
# #     if isinstance(data, list) and all(isinstance(i, str) for i in data):
# #         return [Document(page_content=i) for i in data if i.strip()]

# #     # list of documents
# #     if isinstance(data, list) and all(isinstance(i, Document) for i in data):
# #         return data

# #     raise TypeError(f"❌ Unsupported input type: {type(data)}")


# # # ==============================
# # # TEXT SPLITTING
# # # ==============================

# # def split_documents(docs: List[Document]) -> List[Document]:
# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=CHUNK_SIZE,
# #         chunk_overlap=CHUNK_OVERLAP
# #     )

# #     chunks = splitter.split_documents(docs)

# #     if not chunks:
# #         raise ValueError("❌ No chunks created. Check input text.")

# #     print(f"✅ Chunks created: {len(chunks)}")
# #     return chunks


# # # ==============================
# # # EMBEDDINGS
# # # ==============================

# # def get_embeddings():
# #     return HuggingFaceEmbeddings(
# #         model_name=EMBEDDING_MODEL
# #     )


# # # ==============================
# # # VECTOR STORE (FAISS)
# # # ==============================

# # def create_vectorstore(chunks: List[Document]) -> FAISS:
# #     embeddings = get_embeddings()

# #     vectorstore = FAISS.from_documents(chunks, embeddings)

# #     print(f"✅ FAISS vectorstore created with {len(chunks)} chunks")
# #     return vectorstore


# # # ==============================
# # # MAIN PIPELINE
# # # ==============================

# # def build_rag_pipeline(raw_input: Any) -> Tuple[FAISS, Any]:
# #     """
# #     Full pipeline:
# #     raw input → normalize → split → embeddings → FAISS → retriever
# #     """

# #     print("\n🚀 Starting RAG pipeline...")

# #     docs = normalize_input(raw_input)
# #     print(f"📄 Documents loaded: {len(docs)}")

# #     chunks = split_documents(docs)

# #     vectorstore = create_vectorstore(chunks)

# #     retriever = vectorstore.as_retriever(
# #         search_kwargs={"k": TOP_K}
# #     )

# #     print("✅ RAG pipeline ready\n")

# #     return vectorstore, retriever


# # # ==============================
# # # RETRIEVAL
# # # ==============================

# # def retrieve_context(retriever, query: str) -> str:
# #     docs = retriever.get_relevant_documents(query)

# #     if not docs:
# #         return "No relevant context found."

# #     return "\n\n".join([doc.page_content for doc in docs])


# # # ==============================
# # # QUESTION ANSWERING
# # # ==============================

# # def ask_question(retriever, query: str, llm=None) -> str:
# #     """
# #     RAG QA system
# #     """

# #     context = retrieve_context(retriever, query)

# #     # fallback mode (NO LLM)
# #     if llm is None:
# #         return f"📌 Retrieved Context:\n\n{context}"

# #     prompt = f"""
# # You are a helpful assistant.

# # Use the context below to answer the question.

# # Context:
# # {context}

# # Question:
# # {query}

# # Answer clearly and concisely.
# # """

# #     return llm.invoke(prompt)















# # ---------------------------------------------------------------------------------------------------------------







# import re
# import math
# from collections import Counter
# from typing import List, Dict, Any, Tuple


# # -----------------------------
# # TEXT SPLITTING (simple + safe)
# # -----------------------------
# def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
#     if not isinstance(text, str):
#         text = str(text)

#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + chunk_size
#         chunks.append(text[start:end])
#         start = end - overlap

#         if start < 0:
#             start = 0

#     return chunks


# # -----------------------------
# # TOKENIZATION + VECTOR
# # -----------------------------
# def tokenize(text: str) -> List[str]:
#     return re.findall(r"\b\w+\b", text.lower())


# def vectorize(text: str) -> Counter:
#     return Counter(tokenize(text))


# def cosine_similarity(vec1: Counter, vec2: Counter) -> float:
#     intersection = set(vec1.keys()) & set(vec2.keys())

#     dot_product = sum(vec1[x] * vec2[x] for x in intersection)

#     norm1 = math.sqrt(sum(v * v for v in vec1.values()))
#     norm2 = math.sqrt(sum(v * v for v in vec2.values()))

#     if norm1 == 0 or norm2 == 0:
#         return 0.0

#     return dot_product / (norm1 * norm2)


# # -----------------------------
# # RAG PIPELINE BUILDER (FIXED)
# # -----------------------------
# def build_rag_pipeline(text: str) -> Tuple[Dict[str, Any], None]:
#     """
#     Returns:
#     vectorstore (your index) + rag_llm (None placeholder)
#     """

#     chunks = split_text(text)

#     index = []
#     for chunk in chunks:
#         index.append({
#             "text": chunk,
#             "vector": vectorize(chunk)
#         })

#     vectorstore = {"index": index}

#     # placeholder (so Streamlit unpacking works)
#     rag_llm = None

#     return vectorstore, rag_llm


# # -----------------------------
# # RETRIEVAL
# # -----------------------------
# def retrieve(query: str, rag_data: Dict[str, Any], top_k: int = 3) -> List[str]:
#     query_vec = vectorize(query)

#     scored_chunks = []

#     for item in rag_data["index"]:
#         score = cosine_similarity(query_vec, item["vector"])
#         scored_chunks.append((score, item["text"]))

#     scored_chunks.sort(reverse=True, key=lambda x: x[0])

#     return [text for _, text in scored_chunks[:top_k]]


# # -----------------------------
# # SIMPLE QA
# # -----------------------------
# def answer_query(query: str, rag_data: Dict[str, Any]) -> str:
#     top_chunks = retrieve(query, rag_data)

#     if not top_chunks:
#         return "No relevant information found."

#     return "\n\n".join(top_chunks)








# # ----------------------------------------------------------------------------------------------------

# import re
# import numpy as np
# from typing import List

# # -----------------------------
# # SAFE EMBEDDINGS (OPTIONAL)
# # -----------------------------
# try:
#     from sentence_transformers import SentenceTransformer
#     MODEL = SentenceTransformer("all-MiniLM-L6-v2")
#     USE_ST = True
# except Exception:
#     USE_ST = False
#     MODEL = None


# # -----------------------------
# # PIPELINE CLASS
# # -----------------------------
# class RAGPipeline:

#     def __init__(self, chunk_size: int = 500, overlap: int = 50):
#         self.chunk_size = chunk_size
#         self.overlap = overlap

#         self.text_chunks: List[str] = []
#         self.embeddings = None

#     # -------------------------
#     # TEXT SPLITTER
#     # -------------------------
#     def split_text(self, text: str) -> List[str]:
#         text = re.sub(r"\s+", " ", text)

#         chunks = []
#         start = 0

#         while start < len(text):
#             end = start + self.chunk_size
#             chunks.append(text[start:end])
#             start += self.chunk_size - self.overlap

#         return chunks

#     # -------------------------
#     # EMBEDDINGS
#     # -------------------------
#     def embed(self, texts: List[str]):

#         if USE_ST:
#             return MODEL.encode(texts)

#         # fallback: simple bag-of-words style vectors
#         return np.array([self._simple_vector(t) for t in texts])

#     def _simple_vector(self, text: str):
#         words = text.lower().split()
#         vec = np.zeros(300)

#         for i, w in enumerate(words[:300]):
#             vec[i % 300] += hash(w) % 10

#         return vec

#     # -------------------------
#     # INGEST DATA
#     # -------------------------
#     def ingest(self, text: str):
#         self.text_chunks = self.split_text(text)

#         if not self.text_chunks:
#             raise ValueError("No text chunks created")

#         self.embeddings = self.embed(self.text_chunks)

#     # -------------------------
#     # SIMILARITY SEARCH
#     # -------------------------
#     def _search(self, query: str, top_k: int = 3):

#         if self.embeddings is None:
#             raise ValueError("No documents ingested. Call ingest() first.")

#         query_vec = self.embed([query])[0]

#         scores = []

#         for i, emb in enumerate(self.embeddings):
#             sim = self._cosine_similarity(query_vec, emb)
#             scores.append((sim, self.text_chunks[i]))

#         scores.sort(reverse=True, key=lambda x: x[0])

#         return [text for _, text in scores[:top_k]]

#     def _cosine_similarity(self, a, b):
#         a = np.array(a)
#         b = np.array(b)

#         if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
#             return 0

#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

#     # -------------------------
#     # MAIN QA METHOD (FIX FOR YOUR ERROR)
#     # -------------------------
#     def ask(self, question: str) -> str:

#         top_chunks = self._search(question, top_k=3)

#         context = "\n\n".join(top_chunks)

#         return (
#             "📌 Based on your document:\n\n"
#             f"{context}\n\n"
#             "💡 Answer (Extracted Context Above)"
#         )


# #     ------------------------------------------------------------------------------------------------------------------------

# # app/rag_pipeline.py

# from langchain_core.documents import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings

# from typing import List, Tuple


# # -----------------------------
# # TEXT SPLITTING
# # -----------------------------
# def split_text(text: str) -> List[Document]:
#     """
#     Splits raw text into LangChain Documents.
#     """
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_text(text)

#     return [Document(page_content=chunk) for chunk in chunks]


# # -----------------------------
# # EMBEDDINGS MODEL
# # -----------------------------
# def get_embeddings():
#     """
#     Uses a lightweight local embedding model.
#     """
#     return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# # -----------------------------
# # BUILD VECTOR STORE
# # -----------------------------
# def build_vectorstore(documents: List[Document]):
#     """
#     Creates FAISS vector database from documents.
#     """
#     embeddings = get_embeddings()

#     vectorstore = FAISS.from_documents(
#         documents=documents,
#         embedding=embeddings
#     )

#     return vectorstore


# # -----------------------------
# # RETRIEVAL FUNCTION
# # -----------------------------
# def retrieve_relevant_docs(vectorstore, query: str, k: int = 4):
#     """
#     Retrieves top-k similar chunks for a query.
#     """
#     retriever = vectorstore.as_retriever(search_kwargs={"k": k})
#     return retriever.get_relevant_documents(query)


# # -----------------------------
# # SIMPLE RAG PIPELINE WRAPPER
# # -----------------------------
# def build_rag_pipeline(text: str):
#     """
#     End-to-end pipeline: text → chunks → vectorstore
#     """
#     docs = split_text(text)
#     vectorstore = build_vectorstore(docs)

#     return vectorstore


# # -----------------------------
# # QUERY FUNCTION (MAIN USE)
# # -----------------------------
# def ask_rag(vectorstore, query: str, k: int = 4) -> List[Tuple[str, float]]:
#     """
#     Returns relevant chunks (text only version).
#     """
#     docs = retrieve_relevant_docs(vectorstore, query, k)

#     return [(doc.page_content, 1.0) for doc in docs]



# -------------------------------------------------------------------------------






import re
import math
from collections import Counter
from typing import List, Dict, Any


# -----------------------------
# TEXT PROCESSING
# -----------------------------
def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    if not isinstance(text, str):
        text = str(text)

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0

    return chunks


def tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


def vectorize(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_similarity(vec1: Counter, vec2: Counter) -> float:
    intersection = set(vec1.keys()) & set(vec2.keys())

    dot_product = sum(vec1[x] * vec2[x] for x in intersection)

    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


# -----------------------------
# RAG PIPELINE CLASS (FIXED)
# -----------------------------
class RAGPipeline:
    def __init__(self):
        self.index = []

    # -------------------------
    # INGEST DOCUMENT
    # -------------------------
    def ingest(self, text: str):
        chunks = split_text(text)

        self.index = [
            {
                "text": chunk,
                "vector": vectorize(chunk)
            }
            for chunk in chunks
        ]

    # -------------------------
    # RETRIEVAL
    # -------------------------
    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        query_vec = vectorize(query)

        scored = []

        for item in self.index:
            score = cosine_similarity(query_vec, item["vector"])
            scored.append((score, item["text"]))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [text for _, text in scored[:top_k]]

    # -------------------------
    # MAIN QA FUNCTION
    # -------------------------
    def ask(self, question: str) -> str:
        chunks = self.retrieve(question)

        if not chunks:
            return "No relevant information found."

        return "\n\n".join(chunks)