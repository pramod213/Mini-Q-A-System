import streamlit as st


def pdf_uploader():
    """
    Handles PDF upload in Streamlit UI
    Returns uploaded file(s)
    """
    uploaded_files = st.file_uploader(
        "📤 Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    return uploaded_files