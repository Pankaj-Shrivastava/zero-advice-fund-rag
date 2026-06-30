import requests
import json
import time

def test_api():
    print("Waiting for server to start...")
    for _ in range(10):
        try:
            res = requests.get("http://localhost:8000/api/health")
            if res.status_code == 200:
                print("Server is up!")
                break
        except requests.ConnectionError:
            time.sleep(1)
    else:
        print("Server failed to start in time.")
        return

    print("\n--- Testing Health Endpoint ---")
    res = requests.get("http://localhost:8000/api/health")
    print(f"Status: {res.status_code}")
    print(f"Response: {res.json()}")

    print("\n--- Testing Factual Query ---")
    payload = {"question": "What is the expense ratio of ICICI Prudential Large Cap Fund?"}
    res = requests.post("http://localhost:8000/api/query", json=payload)
    print(f"Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    print("\n--- Testing Advisory Query ---")
    payload = {"question": "Should I invest in ICICI Flexicap?"}
    res = requests.post("http://localhost:8000/api/query", json=payload)
    print(f"Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    print("\n--- Testing Empty Query ---")
    payload = {"question": "   "}
    res = requests.post("http://localhost:8000/api/query", json=payload)
    print(f"Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

if __name__ == "__main__":
    test_api()
