import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "rag_index.faiss"

_model = None
_index = None
_texts = []

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def create_faiss_index(texts):
    global _texts, _index
    _texts = texts
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")
    _index = faiss.IndexFlatL2(embeddings.shape[1])
    _index.add(embeddings)
    faiss.write_index(_index, INDEX_PATH)
    print("FAISS index created and saved.")

def load_faiss_index(texts):
    global _index, _texts
    _texts = texts
    if os.path.exists(INDEX_PATH):
        _index = faiss.read_index(INDEX_PATH)
        print("FAISS index loaded from disk.")
    else:
        create_faiss_index(texts)

def retrieve(query, k=3):
    global _index, _texts
    if _index is None:
        raise ValueError("FAISS index not loaded. Call load_faiss_index first.")
    model = get_model()
    query_vector = model.encode([query]).astype("float32")
    D, I = _index.search(query_vector, k)
    results = [ _texts[i] for i in I[0] if i < len(_texts) ]
    return results
