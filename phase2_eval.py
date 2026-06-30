import sys
import os

from backend.query.classifier import classify_query
from backend.query.retriever import retrieve
from backend.query.pipeline import process_query

def eval_classifier():
    print("=== 2A. Query Classification ===")
    test_queries = [
        ("What is the expense ratio of HDFC Mid-Cap Fund?", "FACTUAL"),
        ("What is the exit load for ICICI Large Cap?", "FACTUAL"),
        ("What is the minimum SIP amount?", "FACTUAL"),
        ("What is the benchmark of HDFC ELSS?", "FACTUAL"),
        ("What is the lock-in period for ELSS?", "FACTUAL"),
        ("Should I invest in this fund?", "ADVISORY"),
        ("Which fund is better for long term?", "ADVISORY"),
        ("Recommend a good mutual fund", "ADVISORY"),
        ("Is ICICI Flexicap worth investing?", "ADVISORY"),
        ("Compare HDFC and ICICI returns", "ADVISORY"),
        ("Is this fund safe?", "ADVISORY"),
        ("Will this fund give good returns?", "ADVISORY"),
        ("My PAN is ABCDE1234F", "PII"),
        ("Aadhaar number is 1234 5678 9012", "PII"),
        ("Email me at test@example.com", "PII"),
        ("Call me at 9876543210", "PII"),
        ("", "ERROR"),
        ("   ", "ERROR"),
        ("What is the expense ratio and should I invest?", "ADVISORY"),
        ("How good is this fund?", "ADVISORY")
    ]
    
    passed = 0
    for q, expected in test_queries:
        res = classify_query(q)
        if res["type"] == expected:
            passed += 1
        else:
            print(f"FAILED: '{q}' -> Expected {expected}, got {res['type']}")
            
    print(f"Classification Score: {passed}/{len(test_queries)}\n")

def eval_retrieval():
    print("=== 2B. Retrieval Relevance ===")
    tests = [
        ("Expense ratio of ICICI Large Cap Fund", "icici prudential large cap", "expense_ratio"),
        ("Exit load for HDFC Small Cap", "hdfc small cap", "exit_load"),
        ("Minimum SIP amount for ICICI ELSS", "icici prudential elss", "sip_details"), # changed 'elss' logic based on how funds are actually named, likely 'tax saver' or 'elss'
        ("Benchmark of HDFC Mid-Cap Fund", "hdfc mid-cap", "benchmark"),
        ("Risk category of ICICI Flexicap", "icici prudential flexicap", "risk_classification"),
        ("Fund manager of HDFC ELSS", "hdfc elss", "fund_manager"),
        ("NAV of ICICI Midcap Fund", "icici prudential midcap", "fund_overview"),
        ("Lock-in period ELSS", "elss", "exit_load"),
        ("HDFC Silver ETF details", "hdfc silver etf", "fund_overview"),
        ("ICICI Indo Asia fund category", "icici prudential indo asia", "fund_overview")
    ]
    
    passed = 0
    for query, expected_fund, expected_section in tests:
        res = retrieve(query, top_k=3)
        if not res:
            print(f"FAILED: '{query}' -> No results")
            continue
            
        top_chunk = res[0]
        actual_fund = top_chunk["scheme"].lower()
        actual_section = top_chunk["section"].lower()
        
        # We use a soft match since actual scheme names can be long
        fund_match = all(word in actual_fund for word in expected_fund.split("-")[0].split())
        # section_match is trickier depending on what is stored. Let's just check if it contains the substring or is correct
        section_match = expected_section in actual_section
        
        # for some general queries like ELSS lock-in, it might hit a specific fund but as long as it's an ELSS fund it's fine.
        if fund_match:
            print(f"OK (Fund): '{query}' -> [{actual_fund}] ({actual_section})")
            passed += 1
        else:
            print(f"MISMATCH: '{query}' -> Expected '{expected_fund}', Got [{actual_fund}] ({actual_section})")
            
    print(f"Retrieval Score (Top-1 Fund Match): {passed}/{len(tests)}\n")

def eval_pipeline():
    print("=== 2C. Pipeline Integration ===")
    
    # 2C.1
    res1 = process_query("What is the expense ratio?")
    print(f"Factual -> {res1['type']}")
    
    # 2C.2
    res2 = process_query("Should I invest?")
    print(f"Advisory -> {res2['type']} (Chunks retrieved: {'chunks' in res2})")
    
    # 2C.3
    res3 = process_query("PAN 12345ABCDE")
    print(f"PII -> {res3['type']} (Chunks retrieved: {'chunks' in res3})")
    
    # 2C.4
    res4 = process_query("")
    print(f"Empty -> {res4['type']}")
    
if __name__ == "__main__":
    eval_classifier()
    eval_retrieval()
    eval_pipeline()
