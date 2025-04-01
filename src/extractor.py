import openai
import json
import time
from config import OPENAI_API_KEY

# Set API key
openai.api_key = OPENAI_API_KEY

def extract_structured_info(text: str, model: str = "gpt-3.5-turbo") -> dict:
    """
    Extract structured information from text using the OpenAI API.
    """
    prompt = (
        "Extract key structured information from the following document:\n\n"
        f"{text[:6000]}\n\n"
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
            temperature=0.0,
        )
        content = response.choices[0].message.content.strip()
        structured_data = json.loads(content)
        return structured_data

    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return {}