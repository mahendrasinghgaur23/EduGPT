import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(uploaded_file):
    """Load a PDF from a Streamlit UploadedFile object."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        return documents
    finally:
        os.unlink(tmp_path)


def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into chunks using RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


def process_pdf(uploaded_file, chunk_size=1000, chunk_overlap=200):
    """Complete pipeline: load PDF -> chunk into documents."""
    documents = load_pdf(uploaded_file)
    chunks = chunk_documents(documents, chunk_size, chunk_overlap)
    return chunks
