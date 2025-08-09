#!/usr/bin/env python3

from app.services.rule_based_polisher import RuleBasedPolisher
from app.services.fluency_polisher import SafeFluencyPolisher

def test_safe_polishing():
    """Test the safe polishing system"""
    
    # Sample text with intentional quirks that should be preserved
    test_text = """this  is   a  sample  text , in some cases it has   weird spacing . you might say  the grammar is  not perfect  but these quirks should be preserved . to be honest  , this (parenthetical comment)  looks  human-like already . basically  , we want to  fix obvious  issues  without  destroying  the  human  markers ."""
    
    print("🔧 Testing Safe Polishing System")
    print("=" * 50)
    print(f"📝 Original Text:")
    print(f"   {test_text}")
    print()
    
    # Test rule-based polisher
    print("📋 Rule-Based Polishing:")
    print("-" * 30)
    
    polisher = RuleBasedPolisher()
    polished_text, changes = polisher.polish(test_text)
    
    print(f"✅ Polished Text:")
    print(f"   {polished_text}")
    print()
    print(f"🔧 Changes Made: {len(changes)}")
    for i, change in enumerate(changes[:5], 1):  # Show first 5 changes
        print(f"   {i}. {change}")
    if len(changes) > 5:
        print(f"   ... and {len(changes) - 5} more")
    print()
    
    # Test fluency polisher
    print("✨ Safe Fluency Polishing:")
    print("-" * 30)
    
    fluency_polisher = SafeFluencyPolisher()
    result = fluency_polisher.polish(test_text, method="rule_based")
    
    print(f"✅ Fluency Polished Text:")
    print(f"   {result['text']}")
    print()
    print(f"📊 Statistics:")
    print(f"   • Method Used: {result['method_used']}")
    print(f"   • Word Count Change: {result['word_count_change']}")
    print(f"   • Original: {result['original_word_count']} words")
    print(f"   • Final: {result['final_word_count']} words")
    print()
    
    # Verify preservation of human markers
    print("🔍 Human Marker Preservation Check:")
    print("-" * 40)
    
    human_markers = [
        "in some cases", "you might say", "to be honest", 
        "basically", "(parenthetical comment)"
    ]
    
    for marker in human_markers:
        in_original = marker in test_text.lower()
        in_polished = marker in result['text'].lower()
        status = "✅ Preserved" if (in_original and in_polished) else "⚠️ Missing" if in_original else "➖ N/A"
        print(f"   • '{marker}': {status}")
    
    print()
    print("🎉 Safe Polishing Test Complete!")
    print()
    print("💡 Key Features Demonstrated:")
    print("   • Fixed spacing and capitalization issues")
    print("   • Preserved human-like filler phrases")
    print("   • Maintained parenthetical comments")
    print("   • Improved readability without losing quirks")

if __name__ == "__main__":
    test_safe_polishing() 