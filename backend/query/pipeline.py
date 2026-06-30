import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.query.classifier import classify_query
from backend.query.retriever import retrieve

def process_query(question: str) -> dict:
    if not question or not question.strip():
        return {"type": "ERROR", "query": question, "message": "Query cannot be empty."}
        
    # 1. Classify the query
    classification = classify_query(question)
    
    if classification["type"] in ["ADVISORY", "PII", "ERROR"]:
        # Skip retrieval
        return classification
        
    # 2. Retrieval (only for FACTUAL)
    retrieved_chunks = retrieve(question, top_k=3)
    
    if not retrieved_chunks:
        return {"type": "NO_CONTEXT", "query": question}
        
    return {
        "type": "FACTUAL",
        "query": question,
        "chunks": retrieved_chunks
    }

if __name__ == "__main__":
    # Test Factual
    res1 = process_query("What is the expense ratio of ICICI Prudential Large Cap Fund?")
    print("Factual Result Type:", res1["type"])
    if "chunks" in res1:
        print(f"Retrieved {len(res1['chunks'])} chunks")
        
    # Test Advisory
    res2 = process_query("Should I invest in ICICI Flexicap?")
    print("\nAdvisory Result Type:", res2["type"])
    
    # Test PII
    res3 = process_query("My PAN is ABCDE1234F")
    print("\nPII Result Type:", res3["type"])
