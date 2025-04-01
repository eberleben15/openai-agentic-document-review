# storage.py
import faiss
import numpy as np
import pickle
import os

INDEX_PATH = "embeddings.index"
DATA_PATH = "doc_data.pkl"

def initialize_index(dimension: int = 1536):
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    return faiss.IndexFlatL2(dimension)

def save_embedding(index, embedding: np.ndarray, metadata: dict):
    embeddings, data = load_data()
    embeddings.append(embedding)
    data.append(metadata)

    embeddings_array = np.array(embeddings).astype('float32')
    index.reset()
    index.add(embeddings_array)

    faiss.write_index(index, INDEX_PATH)
    with open(DATA_PATH, 'wb') as f:
        pickle.dump(data, f)

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'rb') as f:
            data = pickle.load(f)
        embeddings = [d["embedding"] for d in data]
    else:
        data = []
        embeddings = []
    return embeddings, data