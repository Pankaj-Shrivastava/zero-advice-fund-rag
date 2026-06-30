import os
import chromadb
from sentence_transformers import SentenceTransformer
import sys

# Hack to allow running as a script from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL_NAME

# Initialize globally to avoid reloading on every query
_model = None
_chroma_client = None
_collection = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model

def get_collection():
    global _chroma_client, _collection
    if _chroma_client is None:
        # Resolve absolute path for chroma DB based on config (which is relative to project root)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        db_path = os.path.join(project_root, CHROMA_DB_PATH)
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"ChromaDB not found at {db_path}")
        _chroma_client = chromadb.PersistentClient(path=db_path)
        _collection = _chroma_client.get_collection(COLLECTION_NAME)
    return _collection

def extract_metadata_filter(query: str) -> dict:
    query_lower = query.lower()
    
    # Very basic heuristic for metadata filtering
    filters = []
    
    if "hdfc" in query_lower:
        filters.append({"amc": "HDFC Mutual Fund"})
    if "icici" in query_lower:
        filters.append({"amc": "ICICI Prudential"})
        
    if len(filters) == 1:
        return filters[0]
    elif len(filters) > 1:
        # If both are mentioned
        return {"$or": filters}
    
    return {}

def retrieve(query: str, top_k: int = 3) -> list:
    model = get_model()
    collection = get_collection()
    
    # Prepend BGE query prefix
    query_text = "Represent this sentence for searching relevant passages: " + query
    query_emb = model.encode([query_text], normalize_embeddings=True).tolist()
    
    where_filter = extract_metadata_filter(query)
    
    # Query ChromaDB
    kwargs = {
        "query_embeddings": query_emb,
        "n_results": top_k
    }
    if where_filter:
        kwargs["where"] = where_filter
        
    results = collection.query(**kwargs)
    
    # Format results
    retrieved_chunks = []
    if not results['documents'] or not results['documents'][0]:
        return retrieved_chunks
        
    docs = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]
    
    for doc, meta, dist in zip(docs, metadatas, distances):
        chunk = {
            "text": doc,
            "source_url": meta.get("source_url"),
            "amc": meta.get("amc"),
            "scheme": meta.get("scheme"),
            "section": meta.get("section"),
            "score": dist
        }
        retrieved_chunks.append(chunk)
        
    return retrieved_chunks

if __name__ == "__main__":
    res = retrieve("What is the expense ratio of ICICI Prudential Large Cap Fund?")
    for r in res:
        print(f"[{r['scheme']}] score={r['score']:.3f} | {r['text'][:80].replace(chr(10), ' ')}...")
