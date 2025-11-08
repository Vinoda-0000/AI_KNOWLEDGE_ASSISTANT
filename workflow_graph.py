# #Handles data extraction from .pdf, .txt, .csv → inserts into DB → creates FAISS index.
import os
import csv
import fitz  #PyMuPDF
import pandas as pd
from db_module import create_table, insert_document, fetch_all_texts
from rag_module import create_faiss_index

DATA_PATH = "data"

def extract_text_from_file(path):
    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext == ".pdf":
        text = ""
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
        return text
    
    elif ext in [".txt", ".md"]:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
        
    elif ext == ".csv":
        df = pd.read_csv(path)
        return df.to_string(index=False)
    
    else:
        return ""
    
def ingest_data():
    create_table()
    files = os.listdir(DATA_PATH)
    texts = []

    for file in files:
        path = os.path.join(DATA_PATH, file)
        if os.path.isfile(path):
            content = extract_text_from_file(path)
            if content:
                insert_document(file, content)
                texts.append(content)
                print(f"Added {file} ({len(content)} chars)")

    if texts:
        create_faiss_index(texts)
        print("Ingestion & Embedding complete.")
    else:
        print("No files found in data/")
