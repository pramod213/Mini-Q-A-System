# import streamlit as st
# from rag_pipeline import RAGPipeline

# st.set_page_config(page_title="Mini Q&A RAG System", layout="wide")

# st.title("📚 Mini Q&A RAG System")

# # -----------------------------
# # SESSION STATE
# # -----------------------------
# if "rag" not in st.session_state:
#     st.session_state.rag = RAGPipeline()

# if "docs_loaded" not in st.session_state:
#     st.session_state.docs_loaded = False


# # -----------------------------
# # FILE UPLOAD
# # -----------------------------
# st.sidebar.header("📂 Upload Knowledge Base")

# uploaded_file = st.sidebar.file_uploader("Upload .txt file", type=["txt"])

# if uploaded_file:
#     text = uploaded_file.read().decode("utf-8")

#     try:
#         # IMPORTANT: your pipeline must have this method
#         st.session_state.rag.ingest(text)
#         st.session_state.docs_loaded = True
#         st.sidebar.success("✅ Document loaded successfully!")

#     except Exception as e:
#         st.sidebar.error(f"❌ Error: {str(e)}")


# # -----------------------------
# # QUESTION SECTION
# # -----------------------------
# st.subheader("💬 Ask a Question")

# question = st.text_input("Type your question here")

# if st.button("Get Answer"):

#     if not st.session_state.docs_loaded:
#         st.warning("⚠️ Please upload a document first.")
#         st.stop()

#     if not question.strip():
#         st.warning("⚠️ Enter a valid question.")
#         st.stop()

#     try:
#         # 🔥 ONLY ONE EXPECTED METHOD
#         answer = st.session_state.rag.ask(question)

#         st.markdown("### 🧠 Answer")
#         st.write(answer)

#     except Exception as e:
#         st.error(f"❌ Error generating answer: {str(e)}")











# --------------------------------------------------





# import streamlit as st
# from rag_pipeline import RAGPipeline

# st.set_page_config(page_title="Mini Q&A RAG System", layout="wide")

# st.title("📚 Mini Q&A RAG System")

# # -----------------------------
# # SESSION STATE INIT
# # -----------------------------
# if "rag" not in st.session_state:
#     st.session_state.rag = None

# # -----------------------------
# # FILE UPLOAD
# # -----------------------------
# st.sidebar.header("📂 Setup Knowledge Base")

# uploaded_file = st.sidebar.file_uploader(
#     "Upload your document (txt/pdf already processed in your pipeline)",
#     type=["txt", "pdf"]
# )

# # -----------------------------
# # BUILD RAG PIPELINE
# # -----------------------------
# if uploaded_file and st.session_state.rag is None:
#     st.sidebar.success("File uploaded. Building knowledge base...")

#     text = uploaded_file.read().decode("utf-8", errors="ignore")

#     from langchain_text_splitters import RecursiveCharacterTextSplitter
#     from langchain_community.vectorstores import FAISS
#     from langchain_community.embeddings import FakeEmbeddings

#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunks = splitter.split_text(text)

#     embeddings = FakeEmbeddings()
#     vectorstore = FAISS.from_texts(chunks, embeddings)

#     retriever = vectorstore.as_retriever()

#     # IMPORTANT FIX: wrap retriever
#     st.session_state.rag = RAGPipeline(retriever)

#     st.sidebar.success("Knowledge base ready ✅")

# # -----------------------------
# # QUESTION SECTION
# # -----------------------------
# st.subheader("💬 Ask a Question")

# question = st.text_input("Enter your question")

# if st.button("Ask"):

#     if not st.session_state.rag:
#         st.warning("Please upload a document first.")

#     elif not question.strip():
#         st.warning("Please enter a question.")

#     else:
#         answer = st.session_state.rag.ask(question)
#         st.markdown("### 📌 Answer")
#         st.write(answer)









# ---------------------------------------------------------------------------------------------------------------







# import streamlit as st

# # Your updated RAG pipeline
# from app.rag_pipeline import build_rag_pipeline

# # Optional PDF loader (you can replace with your own)
# from pypdf import PdfReader


# # =========================
# # PDF LOADER (SAFE + SIMPLE)
# # =========================
# def load_pdf(file):
#     text = ""
#     pdf = PdfReader(file)

#     for page in pdf.pages:
#         text += page.extract_text() or ""

#     return text


# # =========================
# # STREAMLIT UI CONFIG
# # =========================
# st.set_page_config(
#     page_title="Mini RAG Q&A System",
#     page_icon="🤖",
#     layout="wide"
# )

# st.title("🤖 Mini RAG Q&A System (FAISS + HF Models)")
# st.write("Upload PDFs and ask questions using AI retrieval-augmented generation.")


# # =========================
# # SESSION STATE INIT
# # =========================
# if "rag" not in st.session_state:
#     st.session_state.rag = None

# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None


# # =========================
# # FILE UPLOAD
# # =========================
# uploaded_files = st.file_uploader(
#     "Upload PDF files",
#     type=["pdf"],
#     accept_multiple_files=True
# )

# docs = []

# if uploaded_files:
#     for file in uploaded_files:
#         text = load_pdf(file)
#         docs.append(text)

#     st.success(f"{len(docs)} file(s) loaded successfully.")


# # =========================
# # BUILD RAG PIPELINE
# # =========================
# if docs and st.session_state.rag is None:
#     with st.spinner("Building RAG pipeline..."):
#         vectorstore, rag_llm = build_rag_pipeline(docs)

#         st.session_state.vectorstore = vectorstore
#         st.session_state.rag = rag_llm

#     st.success("RAG system ready! Ask your questions below.")


# # =========================
# # CHAT INPUT
# # =========================
# st.divider()

# question = st.text_input("💬 Ask a question from your documents:")

# if st.button("Get Answer"):
#     if st.session_state.rag is None:
#         st.warning("Please upload documents first.")
#     elif not question:
#         st.warning("Please enter a question.")
#     else:
#         with st.spinner("Thinking..."):
#             docs = st.session_state.rag.get_relevant_documents(question)
#             answer = "\n\n".join([doc.page_content for doc in docs])

#         st.subheader("📌 Answer:")
#         st.write(answer)


# # =========================
# # DEBUG: VIEW CHUNKS (OPTIONAL)
# # =========================
# with st.expander("🔍 Debug: View stored chunks"):
#     if "chunks" in st.session_state and st.session_state.chunks:

#         st.write(f"Total chunks: {len(st.session_state.chunks)}")

#         for i, chunk in enumerate(st.session_state.chunks[:10]):
#             st.markdown(f"### Chunk {i+1}")
#             st.write(
#                 chunk.page_content if hasattr(chunk, "page_content") else str(chunk)
#             )

#     else:
#         st.warning("No chunks found. Upload and process documents first.")









# ------------------------------------------------------------------------








# import streamlit as st
# import sys
# import os

# # Ensure local imports work
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# # Safe import (prevents crash if module missing)
# try:
#     from app.rag_pipeline import build_rag_pipeline
# except Exception as e:
#     st.error(f"Import Error: {e}")
#     st.stop()

# from pypdf import PdfReader


# # =========================
# # PDF LOADER
# # =========================
# def load_pdf(file):
#     text = ""
#     pdf = PdfReader(file)

#     for page in pdf.pages:
#         page_text = page.extract_text()
#         if page_text:
#             text += page_text + "\n"

#     return text.strip()


# # =========================
# # STREAMLIT CONFIG
# # =========================
# st.set_page_config(
#     page_title="Mini RAG Q&A System",
#     page_icon="🤖",
#     layout="wide"
# )

# st.title("🤖 Mini RAG Q&A System")
# st.write("Upload PDFs and ask questions using retrieval-based AI.")


# # =========================
# # SESSION STATE
# # =========================
# if "rag" not in st.session_state:
#     st.session_state.rag = None

# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None


# # =========================
# # FILE UPLOAD
# # =========================
# uploaded_files = st.file_uploader(
#     "Upload PDF files",
#     type=["pdf"],
#     accept_multiple_files=True
# )

# docs = []

# if uploaded_files:
#     for file in uploaded_files:
#         text = load_pdf(file)
#         if text:
#             docs.append(text)

#     st.success(f"{len(docs)} document(s) loaded.")


# # =========================
# # BUILD RAG PIPELINE
# # =========================
# if docs and st.session_state.rag is None:
#     with st.spinner("Building RAG pipeline..."):
#         vectorstore, rag = build_rag_pipeline(docs)

#         st.session_state.vectorstore = vectorstore
#         st.session_state.rag = rag

#     st.success("RAG system ready!")


# # =========================
# # QUESTION ANSWERING
# # =========================
# st.divider()

# question = st.text_input("💬 Ask a question from your documents")

# if st.button("Get Answer"):
#     if not st.session_state.rag:
#         st.warning("Please upload PDFs first.")
#     elif not question:
#         st.warning("Enter a question first.")
#     else:
#         with st.spinner("Searching..."):

#             rag = st.session_state.rag

#             # =========================
#             # SAFE RETRIEVAL LOGIC
#             # =========================
#             if hasattr(rag, "invoke"):
#                 result = rag.invoke(question)

#             elif hasattr(rag, "run"):
#                 result = rag.run(question)

#             elif hasattr(rag, "get_relevant_documents"):
#                 docs = rag.get_relevant_documents(question)
#                 result = "\n\n".join(
#                     [d.page_content for d in docs if hasattr(d, "page_content")]
#                 )

#             else:
#                 result = str(rag)

#         st.subheader("📌 Answer")
#         st.write(result)


# # =========================
# # DEBUG VIEW
# # =========================
# with st.expander("🔍 Debug Info"):
#     st.write("Vectorstore:", type(st.session_state.vectorstore))
#     st.write("RAG Object:", type(st.session_state.rag))



# ----------------------------------------------------------------------------------------




import streamlit as st
from app.rag_pipeline import RAGPipeline

st.set_page_config(page_title="Mini Q&A RAG System", layout="wide")

st.title("📚 Mini Q&A RAG System")


# -----------------------------
# SESSION STATE
# -----------------------------
if "rag" not in st.session_state:
    st.session_state.rag = RAGPipeline()

if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False


# -----------------------------
# FILE UPLOAD
# -----------------------------
st.sidebar.header("📂 Upload Knowledge Base")

uploaded_file = st.sidebar.file_uploader("Upload .txt file", type=["txt"])

if uploaded_file:
    try:
        text = uploaded_file.read().decode("utf-8")

        st.session_state.rag.ingest(text)
        st.session_state.docs_loaded = True

        st.sidebar.success("✅ Document loaded successfully!")

    except Exception as e:
        st.sidebar.error(f"❌ Error loading file: {str(e)}")


# -----------------------------
# QUESTION SECTION
# -----------------------------
st.subheader("💬 Ask a Question")

question = st.text_input("Type your question here")

if st.button("Get Answer"):

    if not st.session_state.docs_loaded:
        st.warning("⚠️ Please upload a document first.")
        st.stop()

    if not question.strip():
        st.warning("⚠️ Enter a valid question.")
        st.stop()

    try:
        answer = st.session_state.rag.ask(question)

        st.markdown("### 🧠 Answer")
        st.write(answer)

    except Exception as e:
        st.error(f"❌ Error generating answer: {str(e)}")