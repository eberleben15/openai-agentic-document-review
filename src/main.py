import os
from preprocessing import extract_text_from_file
from extractor import extract_structured_info
from embedding import get_embedding
from storage import initialize_index, save_embedding, load_data
from rag import answer_query

# Adjust DOCUMENTS_FOLDER to point to the correct path
DOCUMENTS_FOLDER = "documents"

def ingest_documents():
    index = initialize_index()

    # Load existing metadata to avoid duplicates
    _, existing_data = load_data()
    existing_titles = {doc["title"] for doc in existing_data}

    for filename in os.listdir(DOCUMENTS_FOLDER):
        file_path = os.path.join(DOCUMENTS_FOLDER, filename)
        if os.path.isfile(file_path) and filename.lower().endswith((".pdf", ".txt")):
            print(f"Processing {filename}...")
            text = extract_text_from_file(file_path)
            if text:
                structured_info = extract_structured_info(text)
                if structured_info.get("title") in existing_titles:
                    print(f"Skipping {filename} (already ingested).")
                    continue

                # Create a combined string for embedding
                embedding_text = f"{structured_info.get('title', '')}\n{structured_info.get('summary', '')}\n{' '.join(structured_info.get('key_points', []))}"
                embedding_vector = get_embedding(embedding_text)

                metadata = {
                    **structured_info,
                    "embedding": embedding_vector.tolist(),
                    "file_path": filename
                }
                save_embedding(index, embedding_vector, metadata)
                print(f"Ingested and stored: {structured_info.get('title', 'Untitled')}\n")
            else:
                print(f"Failed to extract text from {filename}.\n")

def interactive_query():
    print("\nAll documents loaded successfully! Ready for questions.\n")
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.strip().lower() in ('exit', 'quit'):
            break

        answer, docs = answer_query(query)
        print("\nAnswer:", answer)
        print("\nSources:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc.get('title', 'Untitled')} ({doc.get('file_path', 'unknown')})")
        print("\n---\n")

if __name__ == "__main__":
    ingest_documents()
    interactive_query()