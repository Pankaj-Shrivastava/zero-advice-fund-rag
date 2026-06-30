import re

# Regex patterns for PII
PII_PATTERNS = [
    r"[A-Z]{5}[0-9]{4}[A-Z]", # PAN
    r"\b\d{4}\s?\d{4}\s?\d{4}\b", # Aadhaar
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", # Email
    r"\b\d{10}\b", # Phone (10 digits)
]

# Keyword lists for advisory classification
ADVISORY_KEYWORDS = [
    r"\bshould i\b",
    r"\bbetter\b",
    r"\brecommend\b",
    r"\bwhich fund\b",
    r"\binvest", # matches "invest", "investing"
    r"\bworth\b",
    r"\bcompare\b",
    r"\bsafe\b",
    r"\bgood returns\b",
    r"\bhow good\b",
    r"\bbuy\b",
    r"\bsell\b",
]

def classify_query(query: str) -> dict:
    if not query or not query.strip():
        return {"type": "ERROR", "query": query, "message": "Query cannot be empty."}
        
    query_lower = query.lower()
    
    # 1. Check for PII
    for pattern in PII_PATTERNS:
        if re.search(pattern, query, re.IGNORECASE):
            return {"type": "PII", "query": query}
            
    # 2. Check for Advisory
    for keyword in ADVISORY_KEYWORDS:
        if re.search(keyword, query_lower):
            return {"type": "ADVISORY", "query": query}
            
    # 3. Default to Factual
    return {"type": "FACTUAL", "query": query}

if __name__ == "__main__":
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
            
    print(f"Passed {passed}/{len(test_queries)} tests.")
