#!/usr/bin/env python3
"""
Simple test script for the ReHumanizer API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_demo():
    """Test the demo endpoint"""
    print("🔍 Testing demo endpoint...")
    response = requests.get(f"{BASE_URL}/api/humanize/demo")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Sample Input: {data['sample_input']}")
        print(f"Humanized Text: {data['result']['humanized_text']}")
        print(f"AI Score Before: {data['result']['ai_detection_score_before']}")
        print(f"AI Score After: {data['result']['ai_detection_score_after']}")
        print(f"Processing Time: {data['result']['processing_time_ms']}ms")
    else:
        print(f"Error: {response.text}")
    print()

def test_humanize_text():
    """Test the text humanization endpoint"""
    print("🔍 Testing text humanization...")
    
    test_text = "The artificial intelligence system demonstrates remarkable capabilities in natural language processing and text generation. It can analyze complex patterns and generate coherent responses."
    
    payload = {
        "text": test_text
    }
    
    response = requests.post(f"{BASE_URL}/api/humanize/text", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Original Text: {data['original_text']}")
        print(f"Humanized Text: {data['humanized_text']}")
        print(f"AI Score Before: {data['ai_detection_score_before']}")
        print(f"AI Score After: {data['ai_detection_score_after']}")
        print(f"Readability Improvement: {data['readability_improvement']}%")
        print(f"Processing Time: {data['processing_time_ms']}ms")
    else:
        print(f"Error: {response.text}")
    print()

def test_api_docs():
    """Test if API docs are accessible"""
    print("🔍 Testing API documentation...")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ API documentation is accessible")
    else:
        print("❌ API documentation not accessible")
    print()

if __name__ == "__main__":
    print("🚀 ReHumanizer API Test Suite")
    print("=" * 40)
    
    try:
        test_health()
        test_demo()
        test_humanize_text()
        test_api_docs()
        
        print("✅ All tests completed!")
        print("\n📖 API Documentation: http://localhost:8000/docs")
        print("🌐 Health Check: http://localhost:8000/health")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running on http://localhost:8000")
        print("\nTo start the server, run:")
        print("cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error during testing: {e}") 