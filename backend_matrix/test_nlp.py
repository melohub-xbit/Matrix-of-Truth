"""
Quick test for NLP endpoint after fixing dependencies
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_nlp_health():
    """Test the NLP health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/nlp/health")
        print("="*70)
        print("NLP Health Check")
        print("="*70)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"\nResponse:")
        print(json.dumps(data, indent=2))
        print("\n" + "="*70)
        return response.status_code == 200
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_nlp_analyze():
    """Test the NLP analyze endpoint"""
    try:
        print("\n" + "="*70)
        print("NLP Analysis Test")
        print("="*70)
        
        test_text = "Breaking news: Scientists have discovered that the Earth is flat and NASA has been hiding this truth from us."
        
        print(f"\nAnalyzing text: '{test_text[:50]}...'")
        print("This may take a moment as models are loading...")
        
        response = requests.post(
            f"{BASE_URL}/nlp/analyze",
            json={"text": test_text},
            headers={"Content-Type": "application/json"},
            timeout=120  # Increased timeout for model loading
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Success!")
            print(f"\nML Prediction: {data.get('ml_prediction')}")
            print(f"ML Confidence: {data.get('ml_confidence'):.2%}")
            print(f"KG Prediction: {data.get('kg_prediction')}")
            print(f"Gemini Prediction: {data.get('gemini_prediction')}")
        else:
            print(f"\n✗ Error Response:")
            print(response.text)
        
        print("\n" + "="*70)
        return response.status_code == 200
        
    except requests.Timeout:
        print("\n✗ Request timed out. The models might be taking too long to load.")
        print("Try running the test again - subsequent requests should be faster.")
        return False
    except Exception as e:
        print(f"\n✗ Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Testing NLP Endpoint After Dependency Fixes")
    print("="*70 + "\n")
    
    print("Make sure the backend server is running at http://127.0.0.1:8000\n")
    
    # Test health first
    health_ok = test_nlp_health()
    
    if health_ok:
        # Test analysis
        analyze_ok = test_nlp_analyze()
        
        if analyze_ok:
            print("\n✓ All NLP tests passed!")
        else:
            print("\n✗ NLP analysis test failed")
    else:
        print("\n✗ NLP health check failed - server might not be running")
