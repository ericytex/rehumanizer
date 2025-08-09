#!/usr/bin/env python3

import requests
import json
import time

# API Configuration
API_BASE = "http://localhost:8001"

def test_enhanced_system():
    """Test the enhanced AI humanization system"""
    
    test_text = """The artificial intelligence system demonstrates remarkable capabilities in natural language processing and text generation. These sophisticated algorithms can analyze patterns in data with unprecedented accuracy and efficiency. Machine learning technologies are revolutionizing numerous industries by providing innovative solutions for complex problems. The implementation of these systems requires comprehensive understanding of computational linguistics and advanced mathematical frameworks."""
    
    print("🚀 Testing Enhanced AI Humanization System")
    print("=" * 70)
    print(f"📝 Original Text ({len(test_text.split())} words):")
    print(f"   {test_text}")
    print()
    
    # Test the comprehensive pipeline with all enhancements
    print("🎭 Enhanced Comprehensive Pipeline Test")
    print("-" * 50)
    
    payload = {
        "text": test_text,
        "pipeline_type": "comprehensive",
        "education_level": "undergraduate", 
        "paranoid_mode": True,
        "writehuman_mode": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{API_BASE}/api/humanize/text", json=payload, timeout=60)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            humanized = result['humanized_text']
            processing_time = result['processing_time_ms']
            
            print(f"✅ SUCCESS! ({processing_time}ms API + {int((end_time - start_time) * 1000)}ms total)")
            print(f"📊 Word Count: {len(test_text.split())} → {len(humanized.split())} words")
            print()
            print("🎯 Enhanced Humanized Result:")
            print("─" * 50)
            print(f"{humanized}")
            print("─" * 50)
            print()
            
            # Show pipeline components used
            if 'paraphrased_text' in result:
                print(f"🔧 Pipeline Components Detected:")
                print(f"   • Humaneyes Paraphrasing: ✅")
                print(f"   • Gemini Enhancement: {'✅' if result.get('gemini_humanized_text') else '❌'}")
                print(f"   • Education Level: {result.get('education_level', 'N/A')}")
                print(f"   • Meaning Preserved: {'✅' if result.get('meaning_preserved', True) else '⚠️'}")
                print()
            
            # Analyze text improvements
            analyze_improvements(test_text, humanized)
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"   {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print()
    print("=" * 70)
    print("🎉 Enhanced System Testing Complete!")
    print()
    print("📈 Expected SurferSEO Improvements:")
    print("   • Detection Score: 52% → <20% (Target: ≤15%)")
    print("   • Semantic Similarity: >85% maintained")
    print("   • Readability: Significantly improved with fluency polishing")
    print("   • Flow: Enhanced with coherence preservation")

def analyze_improvements(original: str, humanized: str):
    """Analyze the improvements made to the text"""
    print("📊 Text Analysis:")
    print(f"   • Original Length: {len(original.split())} words")
    print(f"   • Humanized Length: {len(humanized.split())} words")
    print(f"   • Length Change: {((len(humanized.split()) / len(original.split())) - 1) * 100:.1f}%")
    
    # Count certain features
    original_sentences = len([s for s in original.split('.') if s.strip()])
    humanized_sentences = len([s for s in humanized.split('.') if s.strip()])
    
    print(f"   • Sentence Count: {original_sentences} → {humanized_sentences}")
    
    # Look for humanization markers
    human_markers = [
        "in some cases", "you might say", "to be honest", "from what I've seen",
        "in my opinion", "come to think of it", "basically", "in other words"
    ]
    
    markers_found = sum(1 for marker in human_markers if marker in humanized.lower())
    print(f"   • Human-like Phrases: {markers_found} detected")
    
    # Check for sentence variety
    sentence_lengths = [len(s.split()) for s in humanized.split('.') if s.strip()]
    if sentence_lengths:
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        min_length = min(sentence_lengths)
        max_length = max(sentence_lengths)
        print(f"   • Sentence Variety: {min_length}-{max_length} words (avg: {avg_length:.1f})")
    
    print()

def test_comparison():
    """Test comparison between old and new systems"""
    
    test_text = "The artificial intelligence demonstrates sophisticated capabilities in processing complex data structures efficiently."
    
    print("🔄 System Comparison Test")
    print("-" * 30)
    
    # Test without WriteHuman mode (old system)
    print("📊 Without Enhanced WriteHuman:")
    payload_old = {
        "text": test_text,
        "pipeline_type": "comprehensive",
        "writehuman_mode": False
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/humanize/text", json=payload_old, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"   Result: {result['humanized_text'][:100]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test with WriteHuman mode (new system)
    print("🎭 With Enhanced WriteHuman:")
    payload_new = {
        "text": test_text,
        "pipeline_type": "comprehensive",
        "writehuman_mode": True
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/humanize/text", json=payload_new, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"   Result: {result['humanized_text'][:100]}...")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    # Check if API is available
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is accessible")
            test_enhanced_system()
            print("\n" + "="*50 + "\n")
            test_comparison()
        else:
            print("❌ API not responding correctly")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the server is running on http://localhost:8001") 