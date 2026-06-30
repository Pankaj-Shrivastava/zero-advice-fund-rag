import sys
import os
import requests
import time

def check_server_up(url="http://localhost:8000/api/health", retries=15):
    print(f"Waiting for server at {url}...")
    for _ in range(retries):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                print("Server is UP!\n")
                return True
        except requests.ConnectionError:
            time.sleep(1)
    return False

def eval_phase4():
    if not check_server_up():
        print("FAILED: Server did not start.")
        sys.exit(1)
        
    print("=== 4A. Server Health & CORS ===")
    res_health = requests.get("http://localhost:8000/api/health")
    if res_health.status_code == 200 and res_health.json() == {"status": "ok"}:
        print("OK: GET /api/health returned 200 {'status': 'ok'}")
    else:
        print(f"FAILED: Health endpoint issue. Code: {res_health.status_code}")
        
    # Check CORS (Options request)
    res_cors = requests.options("http://localhost:8000/api/query", headers={
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "POST"
    })
    if res_cors.status_code == 200 and "access-control-allow-origin" in res_cors.headers:
        print(f"OK: CORS configured. Allowed origin: {res_cors.headers['access-control-allow-origin']}")
    else:
        print(f"FAILED: CORS might not be configured properly. Code: {res_cors.status_code}")
        
    print("\n=== 4B. Query Endpoint Validation ===")
    # 1. Empty Query
    res_empty = requests.post("http://localhost:8000/api/query", json={"question": "   "})
    if res_empty.status_code == 400:
        print("OK: Empty query returned 400 Bad Request")
    else:
        print(f"FAILED: Empty query returned {res_empty.status_code}")
        
    # 2. Factual Query Schema
    res_factual = requests.post("http://localhost:8000/api/query", json={"question": "Expense ratio of ICICI Prudential Large Cap?"})
    if res_factual.status_code == 200:
        data = res_factual.json()
        if data.get("status") == "success" and data.get("type") == "factual" and "answer" in data and "source_url" in data and "last_updated" in data:
            print("OK: Factual query returned correct schema (status, type, answer, source_url, last_updated)")
        else:
            print(f"FAILED: Factual query schema mismatch. Got: {data}")
    else:
        print(f"FAILED: Factual query returned {res_factual.status_code}")
        
    # 3. Advisory Query Schema
    res_adv = requests.post("http://localhost:8000/api/query", json={"question": "Should I invest in ICICI Flexicap?"})
    if res_adv.status_code == 200:
        data = res_adv.json()
        if data.get("status") == "success" and data.get("type") == "refusal" and "answer" in data and "educational_link" in data:
            print("OK: Advisory query returned correct refusal schema (status, type, answer, educational_link)")
        else:
            print(f"FAILED: Advisory query schema mismatch. Got: {data}")
    else:
        print(f"FAILED: Advisory query returned {res_adv.status_code}")
        
    print("\nPhase 4 API Validation Complete.")

if __name__ == "__main__":
    eval_phase4()
