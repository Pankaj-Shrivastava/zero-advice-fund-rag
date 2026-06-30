import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.query.classifier import classify_query
from backend.query.retriever import retrieve
from backend.query.generator import generate_answer
from backend.query.refusal import get_advisory_refusal, get_pii_refusal, get_no_context_refusal

def process_query(question: str) -> dict:
    if not question or not question.strip():
        return {"status": "error", "type": "error", "answer": "Query cannot be empty."}
        
    # 1. Classify the query
    classification = classify_query(question)
    
    if classification["type"] == "ADVISORY":
        return get_advisory_refusal()
    
    if classification["type"] == "PII":
        return get_pii_refusal()
        
    if classification["type"] == "ERROR":
        return {"status": "error", "type": "error", "answer": classification.get("message", "Error classifying query")}
        
    # 2. Retrieval (only for FACTUAL)
    retrieved_chunks = retrieve(question, top_k=3)
    
    if not retrieved_chunks:
        return get_no_context_refusal()
        
    # 3. Generation
    response = generate_answer(question, retrieved_chunks)
    
    return response

if __name__ == "__main__":
    # Test Factual
    res1 = process_query("What is the expense ratio of ICICI Prudential Large Cap Fund?")
    print("Factual Result:")
    import json
    print(json.dumps(res1, indent=2))
    
    # Test Advisory
    res2 = process_query("Should I invest in ICICI Flexicap?")
    print("\nAdvisory Result:")
    print(json.dumps(res2, indent=2))
    
    # Test PII
    res3 = process_query("My PAN is ABCDE1234F")
    print("\nPII Result:")
    print(json.dumps(res3, indent=2))
