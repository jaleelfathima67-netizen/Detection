import requests
import json

def test_api():
    url = "http://localhost:8000/api/detect/"
    headers = {"Content-Type": "application/json"}
    
    tests = [
        {"text": "NASA confirms discovery of liquid water on Mars surface in major scientific breakthrough.", "expected": "REAL"},
        {"text": "Secret government satellites are using space lasers to control the weather globally.", "expected": "FAKE"}
    ]
    
    for test in tests:
        try:
            print(f"Testing: {test['text'][:50]}...")
            response = requests.post(url, headers=headers, json={"text": test["text"]}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"Result: {data['label']} (Confidence: {data['confidence']:.2f})")
                print(f"Model Used: {data['model_used']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_api()
