import openai
import numpy as np
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_embedding(text: str, model="text-embedding-ada-002") -> np.ndarray:
    response = openai.Embedding.create(input=text, model=model)
    embedding = response['data'][0]['embedding']
    return np.array(embedding)