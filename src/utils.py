# utils.py
import tiktoken

def count_tokens(text: str, model="gpt-3.5-turbo") -> int:
    """
    Counts tokens in text to monitor API usage.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

