# ingest.py
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def loadAndSplitDoc(file_path):
    pdf_loader = PyPDFLoader(file_path)
    documents = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(documents)

    return documents
