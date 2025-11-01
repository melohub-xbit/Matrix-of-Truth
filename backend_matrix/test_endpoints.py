"""
Simple script to test backend endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}\n")
        return False

def test_all_news():
    """Test the all-news endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/all-news")
        print(f"All News: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"News Count: {len(data.get('content', []))}\n")
        else:
            print(f"Error: {response.text}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"All News Failed: {e}\n")
        return False

def test_fact_check_text():
    """Test the fact-check-text endpoint"""
    try:
        test_text = "The Earth is flat and NASA is hiding the truth."
        response = requests.post(
            f"{BASE_URL}/get-fc-text",
            json={"text": test_text},
            headers={"Content-Type": "application/json"}
        )
        print(f"Fact Check Text: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            if data.get('content'):
                print(f"Has fact check result: Yes\n")
            else:
                print(f"Has fact check result: No\n")
        else:
            print(f"Error: {response.text}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Fact Check Text Failed: {e}\n")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Backend Endpoints")
    print("=" * 50 + "\n")
    
    results = {
        "Health Check": test_health(),
        "All News": test_all_news(),
        "Fact Check Text": test_fact_check_text()
    }
    
    print("=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
