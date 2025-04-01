# main.py
import os
from preprocessing import extract_text_from_file
from extractor import extract_structured_info
from embedding import get_embedding
from storage import initialize_index, save_embedding, load_data
from rag import answer_query

DOCUMENTS_FOLDER = "../documents"

def ingest_documents():
    index = initialize_index()

    existing_data_titles = {doc["title"] for _, docs in [load_data()] for doc in docs}

    for filename in os.listdir(DOCUMENTS_FOLDER):
        file_path = os.path.join(DOCUMENTS_FOLDER, filename)
        
        if os.path.isfile(file_path) and filename.lower().endswith((".pdf", ".txt")):
            print(f"Processing {filename}...")
            text = extract_text_from_file(file_path)

            if text:
                structured_info = extract_structured_info(text)
                
                if structured_info["title"] in existing_data_titles:
                    print(f"Skipping {filename} (already ingested).")
                    continue

                embedding_vector = get_embedding(
                    f"{structured_info['title']}\n{structured_info['summary']}\n{' '.join(structured_info['key_points'])}"
                )

                metadata = {
                    **structured_info,
                    "embedding": embedding_vector.tolist(),
                    "file_path": filename
                }

                save_embedding(index, embedding_vector, metadata)
                print(f"Ingested and stored: {structured_info['title']}\n")
            else:
                print(f"Failed to extract text from {filename}.\n")

def interactive_query():
    print("\nAll documents loaded successfully! Ready for questions.\n")
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.lower() in ('exit', 'quit'):
            break

        answer, docs = answer_query(query)
        print("\nAnswer:", answer)

        print("\nSources:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc['title']} ({doc['file_path']})")
        print("\n---\n")

if __name__ == "__main__":
    ingest_documents()
    interactive_query()