import requests
import time

def check():
    url = "http://127.0.0.1:8000/api/detect/"
    print(f"Checking {url}...")
    try:
        # Just a GET to see if it responds (it should 405 because it's POST only, but it proves it's alive)
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content: {response.text[:200]}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check()
