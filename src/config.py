# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Example for future OpenAI integration:
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")