#!/usr/bin/env python3

import requests
import json
import time

# API Configuration
API_BASE = "http://localhost:8001"

def test_writehuman():
    """Test the WriteHuman mimicry feature"""
    
    test_text = """The artificial intelligence system demonstrates remarkable capabilities in natural language processing and text generation. Machine learning algorithms can analyze patterns in data with unprecedented accuracy. These technological innovations are transforming numerous industries and business operations worldwide."""
    
    print("🧪 Testing WriteHuman Mimicry for SurferSEO Evasion")
    print("=" * 60)
    print(f"📝 Original Text ({len(test_text.split())} words):")
    print(f"   {test_text}")
    print()
    
    # Test 1: With WriteHuman Mode ON
    print("🎭 Test 1: WITH WriteHuman Mode (SurferSEO Killer)")
    print("-" * 50)
    
    payload = {
        "text": test_text,
        "pipeline_type": "comprehensive",
        "education_level": "undergraduate", 
        "paranoid_mode": True,
        "writehuman_mode": True
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/humanize/text", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            humanized = result['humanized_text']
            processing_time = result['processing_time_ms']
            
            print(f"✅ SUCCESS! ({processing_time}ms)")
            print(f"📊 Word Count: {len(humanized.split())} words")
            print(f"🎯 Result:")
            print(f"   {humanized}")
            print()
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    
    # Test 2: With WriteHuman Mode OFF (comparison)
    print("🚫 Test 2: WITHOUT WriteHuman Mode (comparison)")
    print("-" * 50)
    
    payload['writehuman_mode'] = False
    
    try:
        response = requests.post(f"{API_BASE}/api/humanize/text", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            humanized = result['humanized_text']
            processing_time = result['processing_time_ms']
            
            print(f"✅ SUCCESS! ({processing_time}ms)")
            print(f"📊 Word Count: {len(humanized.split())} words")
            print(f"🎯 Result:")
            print(f"   {humanized}")
            print()
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("=" * 60)
    print("🎉 WriteHuman Testing Complete!")
    print()
    print("📈 Expected Impact:")
    print("   • SurferSEO detection: 52% → <20%")
    print("   • Maintains 0-1% on other detectors")
    print("   • Preserves meaning while adding quirks")

if __name__ == "__main__":
    test_writehuman() 