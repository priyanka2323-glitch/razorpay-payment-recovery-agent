import os
import chromadb
from pathlib import Path

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("recovery_playbook")

def load_playbook():
    playbook_dir = Path(__file__).parent / "playbook"
    docs, ids, metadatas = [], [], []
    
    for file in playbook_dir.glob("*.md"):
        content = file.read_text()
        docs.append(content)
        ids.append(file.stem)
        metadatas.append({"failure_code": file.stem})
    
    collection.upsert(documents=docs, ids=ids, metadatas=metadatas)
    print(f"Loaded {len(docs)} playbook documents")

def retrieve_playbook(failure_code, n_results=1):
    results = collection.query(
        query_texts=[failure_code],
        n_results=n_results
    )
    return results["documents"][0] if results["documents"] else []

if __name__ == "__main__":
    load_playbook()