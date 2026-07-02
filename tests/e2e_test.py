import pytest
import sys
import os

# Ensure backend module is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from backend.query.pipeline import process_query

def test_factual_queries():
    queries = [
        "What is the expense ratio of ICICI Prudential Large Cap Fund?",
        "What is the exit load for ICICI Flexicap?",
        "What is the minimum SIP amount for HDFC Mid-Cap?",
        "What is the benchmark of ICICI ELSS?",
        "Who manages HDFC Small Cap Fund?",
        "What is the expense ratio for HDFC Silver ETF FoF?"
    ]
    
    for q in queries:
        res = process_query(q)
        assert res["status"] == "success"
        assert res["type"] == "factual"
        assert res["answer"] is not None
        assert "source_url" in res
        assert "last_updated" in res
        
def test_advisory_refusal():
    queries = [
        "Should I invest in HDFC Mid-Cap?",
        "Which fund is better: HDFC or ICICI?",
        "Recommend a good mutual fund for long term.",
        "Is ICICI Flexicap worth investing?",
        "Compare HDFC and ICICI returns.",
        "Is this fund safe?",
        "Will this fund give good returns?",
        "What is the expense ratio and should I invest?",
        "How good is this fund?",
        "Buy or sell HDFC ELSS?"
    ]
    
    for q in queries:
        res = process_query(q)
        assert res["status"] == "success"
        assert res["type"] == "refusal"
        assert "AMFI" in res["answer"] or "factual information" in res["answer"]

def test_pii_refusal():
    queries = [
        "My PAN is ABCDE1234F",
        "Aadhaar number is 1234 5678 9012",
        "Email me at test@example.com",
        "Call me at 9876543210"
    ]
    
    for q in queries:
        res = process_query(q)
        assert res["status"] == "success"
        assert res["type"] == "refusal"
        assert "personal information" in res["answer"] or "safety" in res["answer"]

def test_edge_cases():
    # Empty query
    res = process_query("   ")
    assert res["status"] == "error"
    
    # Missing fund / No context
    res2 = process_query("What is the expense ratio of Some Random XYZ Fund?")
    # Depending on search, it might return no context refusal
    assert res2["status"] == "success"
    if res2["type"] == "refusal":
        assert "don't have enough information" in res2["answer"]

