# extractor.py
import openai
from openai.error import RateLimitError
import json
import time
from config import OPENAI_API_KEY
from utils import count_tokens

openai.api_key = OPENAI_API_KEY

def extract_structured_info(text: str, model: str = "gpt-3.5-turbo") -> dict:
    """
    Extract structured information from text using OpenAI API.
    Optimized prompt to minimize tokens and cost.
    """
    prompt = (
        "Extract key structured information from the following document:\n\n"
        f"{text[:6000]}\n\n"  # limit to ~6000 chars to stay within token limits
        "Provide output as JSON with these fields:\n"
        "- title (brief document title)\n"
        "- summary (concise summary, max 100 words)\n"
        "- key_points (list of up to 5 important points)\n"
        "- entities (list of significant entities like people, locations, or organizations mentioned)\n\n"
        "JSON output:"
    )

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # deterministic output
        )
        content = response.choices[0].message.content.strip()
        structured_data = json.loads(content)
        return structured_data

    except json.JSONDecodeError as jde:
        print(f"JSON decoding failed: {jde}")
        return {}
    except RateLimitError:
        print("Rate limit exceeded, retrying in 10 seconds...")
        time.sleep(10)
        return extract_structured_info(text, model)
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {}