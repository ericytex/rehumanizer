#!/usr/bin/env python3
"""
Test script for Gemini pipeline integration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.gemini_pipeline import run_advanced_pipeline, run_quick_humanization_pipeline
from app.services.humanizer import AdvancedHumanizer

def test_gemini_pipeline():
    """Test the Gemini pipeline integration"""
    print("🧪 Testing Gemini Pipeline Integration")
    print("=" * 50)
    
    test_text = "The artificial intelligence system demonstrates remarkable capabilities in natural language processing and text generation. It can analyze complex patterns and generate coherent responses that mimic human communication patterns."
    
    print(f"📝 Original text ({len(test_text.split())} words):")
    print(test_text)
    print("\n" + "=" * 50)
    
    # Test Advanced Pipeline
    print("\n🚀 Testing Advanced Pipeline (4-pass)...")
    try:
        advanced_result = run_advanced_pipeline(test_text, "AI technology, machine learning, natural language processing")
        print(f"✅ Advanced pipeline result ({len(advanced_result.split())} words):")
        print(advanced_result)
    except Exception as e:
        print(f"❌ Advanced pipeline failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test Quick Pipeline
    print("\n⚡ Testing Quick Pipeline (3-pass)...")
    try:
        quick_result = run_quick_humanization_pipeline(test_text)
        print(f"✅ Quick pipeline result ({len(quick_result.split())} words):")
        print(quick_result)
    except Exception as e:
        print(f"❌ Quick pipeline failed: {e}")
    
    print("\n" + "=" * 50)
    
    # Test AdvancedHumanizer
    print("\n🔧 Testing AdvancedHumanizer...")
    try:
        humanizer = AdvancedHumanizer()
        result = humanizer.humanize_text(test_text, "advanced")
        print(f"✅ AdvancedHumanizer result:")
        print(f"   - Original: {len(result['original_text'].split())} words")
        print(f"   - Paraphrased: {len(result['paraphrased_text'].split())} words")
        print(f"   - Final: {len(result['humanized_text'].split())} words")
        print(f"   - AI Score: {result['ai_detection_score_before']} → {result['ai_detection_score_after']}")
        print(f"   - Processing time: {result['processing_time_ms']}ms")
    except Exception as e:
        print(f"❌ AdvancedHumanizer failed: {e}")

if __name__ == "__main__":
    test_gemini_pipeline() 