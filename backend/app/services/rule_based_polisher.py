import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

class RuleBasedPolisher:
    """
    Sophisticated rule-based text polisher that improves readability
    while preserving anti-AI detection features.
    """
    
    def __init__(self):
        # Patterns to preserve (DO NOT modify these)
        self.preserve_patterns = [
            r'\b(?:in some cases|you might say|to be honest|from what I\'ve seen|in my opinion|come to think of it)\b',
            r'\([^)]+\)',  # Parenthetical comments
            r'—[^—]+—',    # Em-dash asides
            r'\.{3}',      # Ellipses
            r'\b(?:basically|in other words|what I mean is)\b',  # Redundancy phrases
        ]
        
        # Safe polishing rules (improve readability without destroying quirks)
        self.polish_rules = [
            # Fix spacing issues
            (r'\s+([,.!?;:])', r'\1'),  # Remove space before punctuation
            (r'([,.!?;:])\s{2,}', r'\1 '),  # Normalize space after punctuation
            (r'\s{3,}', r'  '),  # Limit excessive spaces to max 2
            
            # Fix capitalization after sentence endings (removed - handled separately)
            # (r'(\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper()),
            # (r'([!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper()),
            
            # Fix common grammar issues while preserving style
            (r'\b(a)\s+([aeiouAEIOU])', r'an \2'),  # a -> an before vowels
            (r'\b(an)\s+([bcdfgjklmnpqrstvwxyzBCDFGJKLMNPQRSTVWXYZ])', r'a \2'),  # an -> a before consonants
            
            # Fix double punctuation
            (r'([,.!?;:])\1+', r'\1'),  # Remove duplicate punctuation
            
            # Improve sentence flow (very conservative)
            (r'\b(and|but|so|yet)\s+(and|but|so|yet)\b', r'\2'),  # Remove redundant conjunctions
            
            # Fix obvious typos while preserving intended quirks
            (r'\bthe\s+the\b', r'the'),  # Remove "the the"
            (r'\ba\s+a\b', r'a'),  # Remove "a a"
            (r'\ban\s+an\b', r'an'),  # Remove "an an"
        ]
        
        # Transition improvements (help sentences flow better)
        self.transition_improvements = [
            # Add gentle transitions where abrupt
            (r'(\.) ([A-Z][^.!?]*?(?:shows|helps|great|advanced))', r'\1 This \2'),
            (r'(\.) (So\s)', r'\1 \2'),  # Keep "So" transitions
        ]

    def _is_preserved_content(self, text: str, start: int, end: int) -> bool:
        """Check if content in range should be preserved"""
        snippet = text[start:end]
        for pattern in self.preserve_patterns:
            if re.search(pattern, snippet, re.IGNORECASE):
                return True
        return False

    def _apply_safe_rule(self, text: str, pattern: str, replacement) -> str:
        """Apply a polishing rule while avoiding preserved content"""
        try:
            if callable(replacement):
                # Handle lambda functions
                matches = list(re.finditer(pattern, text))
                offset = 0
                for match in matches:
                    start, end = match.span()
                    start += offset
                    end += offset
                    
                    # Check if this area should be preserved
                    if not self._is_preserved_content(text, max(0, start-20), min(len(text), end+20)):
                        old_text = text[start:end]
                        new_text = replacement(match)
                        text = text[:start] + new_text + text[end:]
                        offset += len(new_text) - len(old_text)
            else:
                # Handle string replacements with simple substitution
                if not any(self._is_preserved_content(text, m.start()-20, m.end()+20) 
                          for m in re.finditer(pattern, text)):
                    text = re.sub(pattern, replacement, text)
        except re.error as e:
            # Skip problematic regex patterns
            logger.warning(f"Skipping regex pattern due to error: {pattern} - {e}")
        
        return text

    def polish(self, text: str) -> Tuple[str, List[str]]:
        """
        Apply rule-based polishing while preserving anti-AI features
        
        Returns:
            Tuple of (polished_text, list_of_changes_made)
        """
        logger.info("🔧 Applying rule-based polishing...")
        
        original_text = text
        changes_made = []
        
        # Apply basic polishing rules
        for pattern, replacement in self.polish_rules:
            old_text = text
            text = self._apply_safe_rule(text, pattern, replacement)
            if text != old_text:
                changes_made.append(f"Applied rule: {pattern[:30]}...")
        
        # Apply transition improvements (very carefully)
        for pattern, replacement in self.transition_improvements:
            old_text = text
            text = self._apply_safe_rule(text, pattern, replacement)
            if text != old_text:
                changes_made.append(f"Improved transition")
        
        # Final cleanup - ensure sentences start with capital letters
        sentences = re.split(r'(\.\s+|\!\s+|\?\s+)', text)
        for i in range(0, len(sentences), 2):  # Only actual sentences, not separators
            if sentences[i].strip() and sentences[i][0].islower():
                sentences[i] = sentences[i][0].upper() + sentences[i][1:]
                changes_made.append("Fixed sentence capitalization")
        
        text = ''.join(sentences)
        
        # Ensure proper spacing around preserved elements
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = text.strip()
        
        original_words = len(original_text.split())
        final_words = len(text.split())
        
        logger.info(f"✅ Rule-based polishing complete: {original_words} → {final_words} words")
        
        return text, changes_made 