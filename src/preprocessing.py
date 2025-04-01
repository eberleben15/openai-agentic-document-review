# preprocessing.py
import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
    return text.strip()

def extract_text_from_txt(txt_path: str) -> str:
    """
    Extract text from a TXT file.
    """
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error processing TXT {txt_path}: {e}")
        return ""

def extract_text_from_file(file_path: str) -> str:
    """
    Generic method to extract text based on file extension.
    Supports PDF and TXT, extendable for more types.
    """
    _, ext = os.path.splitext(file_path.lower())

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")