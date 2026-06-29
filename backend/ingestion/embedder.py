import os
import json
import chromadb
from sentence_transformers import SentenceTransformer

INPUT_FILE = os.path.join(os.path.dirname(__file__), "chunked_data.json")
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "../vectorstore")
MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "fund_chunks"
BATCH_SIZE = 64

def embed_and_store():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        chunks = json.load(f)

    if not chunks:
        print("No chunks to embed.")
        return

    print(f"Loading SentenceTransformer model: {MODEL_NAME} ...")
    model = SentenceTransformer(MODEL_NAME)
    
    print(f"Initializing ChromaDB client at {VECTORSTORE_DIR} ...")
    if not os.path.exists(VECTORSTORE_DIR):
        os.makedirs(VECTORSTORE_DIR)
        
    chroma_client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
    
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass
        
    collection = chroma_client.create_collection(name=COLLECTION_NAME)
    
    print(f"Embedding {len(chunks)} chunks in batches of {BATCH_SIZE}...")
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i+BATCH_SIZE]
        
        ids = [chunk["chunk_id"] for chunk in batch]
        documents = [chunk["text"] for chunk in batch]
        metadatas = []
        for chunk in batch:
            meta = {
                "source_url": chunk["source_url"],
                "amc": chunk["amc"],
                "scheme": chunk["scheme"],
                "category": chunk["category"],
                "section": chunk["section"],
                "scraped_at": chunk["scraped_at"]
            }
            metadatas.append(meta)
            
        texts_to_embed = ["Represent this sentence: " + doc for doc in documents]
        embeddings = model.encode(texts_to_embed, normalize_embeddings=True).tolist()
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Stored {min(i + len(batch), len(chunks))}/{len(chunks)} chunks.")
        
    print(f"\nIndexed {len(chunks)} chunks into ChromaDB (collection: '{COLLECTION_NAME}')")

def verify_index():
    chroma_client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
    col = chroma_client.get_collection(COLLECTION_NAME)
    print(f"\nTotal documents in ChromaDB: {col.count()}")
    
    query = "expense ratio HDFC mid cap"
    model = SentenceTransformer(MODEL_NAME)
    
    query_emb = model.encode(["Represent this sentence for searching relevant passages: " + query], normalize_embeddings=True).tolist()
    
    results = col.query(query_embeddings=query_emb, n_results=3)
    
    print(f"\nTest Query: '{query}'")
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        print(f"[{meta['scheme']}] {doc[:80].replace(chr(10), ' ')}...")
        
if __name__ == "__main__":
    embed_and_store()
    verify_index()
