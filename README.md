# 🧠 OpenAI Agentic Document Review

A powerful, containerized document review system that uses OpenAI's GPT models and FAISS to extract, embed, and intelligently answer questions about your PDF and text files. This project is designed for analysts, researchers, and engineers who need to search and interact with the content of many documents—quickly and accurately.

---

## 🔧 Features

- **Automatic Document Ingestion**  
  Load all `.pdf` and `.txt` files from the `documents/` folder on startup.

- **Structured LLM-Based Extraction**  
  Uses OpenAI’s GPT to extract:  
  - Title  
  - Summary  
  - Key Points  
  - Named Entities  

- **Embedding + Retrieval**  
  - Generates embeddings using `text-embedding-ada-002`.  
  - Stores them in a FAISS vector index.  
  - Retrieves relevant context using vector similarity.

- **Interactive Q&A**  
  Ask questions about your documents in a terminal interface using Retrieval-Augmented Generation (RAG).

- **Containerized**  
  Fully Dockerized for reproducibility, deployment, and portability.

---

## 📦 Requirements

- Docker  
- OpenAI API Key

For local development (without Docker):
- Python 3.11  
- `pip install -r requirements.txt`

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/openai-agentic-document-review.git
cd openai-agentic-document-review
```

### 2. Add Your OpenAI API Key

Create a .env file in the root of the repo:
```bash
OPENAI_API_KEY=your-api-key-here
```

### 3. Add Documents

Drop any .pdf or .txt files into the documents/ folder. These will be automatically processed on startup.


### 🐳 Using Docker

Build the Docker Image
```bash
docker build -t openai-agentic-document-review .
```

Run the App
```bash
docker run -it --env-file .env -v $(pwd)/data:/app/data openai-agentic-document-review
```
The app will:
	1.	Ingest all documents.
	2.	Extract and embed their content.
	3.	Enter interactive Q&A mode.


### 🗂️ Project Structure
```bash
openai-agentic-document-review/
├── documents/           # Drop your .pdf or .txt files here
├── data/                # FAISS index and metadata stored here
├── src/
│   ├── main.py          # Ingests docs, runs interactive Q&A
│   ├── preprocessing.py # Text extraction from files
│   ├── extractor.py     # Structured LLM info extraction
│   ├── embedding.py     # Embedding generation (OpenAI)
│   ├── storage.py       # FAISS index + metadata handling
│   ├── rag.py           # RAG interface for Q&A
│   ├── config.py        # Loads .env
│   └── utils.py         # Token counting, helpers
├── Dockerfile
├── .env                 # Your OpenAI API key
├── requirements.txt
└── README.md
```

### 💬 Example Usage
```bash
$ python src/main.py

Processing court-case-23.pdf...
Ingested and stored: Johnson v. State Board

Enter your question (or type 'exit' to quit): What were the main findings of Johnson v. State Board?

Answer:
The court found that the State Board violated procedural due process...

Sources:
1. Johnson v. State Board (court-case-23.pdf)
```

🛠 Tech Stack
	•	OpenAI GPT-3.5 / Embedding API
	•	FAISS for vector search
	•	PyMuPDF for PDF parsing
	•	Python 3.11
	•	Docker

⚠️ Notes
	•	This repo is pinned to openai==0.28.0 for legacy compatibility.
To upgrade to SDK v1.x, see: https://github.com/openai/openai-python/discussions/742
	•	Re-run the container to ingest new documents added to the documents/ folder.

📄 License

MIT License © 2024

🙏 Acknowledgments
	•	OpenAI Python SDK
	•	Facebook FAISS
	•	PyMuPDF