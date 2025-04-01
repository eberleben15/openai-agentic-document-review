# rag.py
import faiss
import numpy as np
import pickle
import openai
from embedding import get_embedding
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

INDEX_PATH = "embeddings.index"
DATA_PATH = "doc_data.pkl"

def retrieve_similar_docs(query: str, top_k=3):
    index = faiss.read_index(INDEX_PATH)
    with open(DATA_PATH, 'rb') as f:
        metadata = pickle.load(f)

    query_emb = get_embedding(query).astype('float32')
    _, indices = index.search(np.array([query_emb]), top_k)

    relevant_docs = []
    for idx in indices[0]:
        if idx < len(metadata):
            relevant_docs.append(metadata[idx])

    return relevant_docs

def generate_answer(query: str, docs: list, model="gpt-3.5-turbo"):
    context_parts = []
    for doc in docs:
        part = (
            f"Title: {doc['title']}\n"
            f"Summary: {doc['summary']}\n"
            f"Key Points: {', '.join(doc['key_points'])}\n"
            f"Entities: {', '.join(doc['entities'])}"
        )
        context_parts.append(part)

    context_text = "\n\n".join(context_parts)

    prompt = (
        f"You have the following documents:\n\n{context_text}\n\n"
        f"Answer the following question clearly using this information:\n{query}\n\nAnswer:"
    )

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    return response.choices[0].message.content.strip()

def answer_query(query: str):
    docs = retrieve_similar_docs(query)
    if docs:
        answer = generate_answer(query, docs)
        return answer, docs
    return "No relevant documents found.", []