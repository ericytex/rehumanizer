import re
import logging
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Try to import Gemini for advanced polishing
try:
    import google.generativeai as genai
    from google.generativeai import GenerativeModel
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

load_dotenv()
logger = logging.getLogger(__name__)

class SafeFluencyPolisher:
    """
    Post-processing fluency polisher that improves readability and coherence
    while carefully preserving anti-AI detection features.
    """
    
    def __init__(self):
        self.gemini_available = False
        
        # Try to initialize Gemini for advanced polishing
        if GEMINI_AVAILABLE:
            try:
                api_key = os.getenv("GEMINI_API_KEY")
                if api_key and api_key != "your_gemini_api_key_here":
                    genai.configure(api_key=api_key)
                    self.model = GenerativeModel("gemini-1.5-pro")
                    self.gemini_available = True
                    logger.info("✅ Gemini model initialized for fluency polishing")
            except Exception as e:
                logger.warning(f"⚠️ Gemini unavailable for polishing: {e}")
        
        # Rule-based polishing patterns
        self.polish_patterns = {
            # Fix obvious grammar issues while preserving quirks
            r'\s+,': ',',  # Fix spacing before commas
            r'\s+\.': '.',  # Fix spacing before periods
            r'(\w+),\s*,': r'\1,',  # Remove duplicate commas
            r'(\w+)\.\s*\.': r'\1.',  # Remove duplicate periods
            r'\s{2,}': ' ',  # Normalize multiple spaces
            r'^([a-z])': lambda m: m.group(1).upper(),  # Capitalize sentence starts
        }

    def _rule_based_polish(self, text: str) -> str:
        """Apply rule-based polishing for basic readability improvements"""
        polished = text
        
        # Apply pattern-based fixes
        for pattern, replacement in self.polish_patterns.items():
            if callable(replacement):
                polished = re.sub(pattern, replacement, polished, flags=re.MULTILINE)
            else:
                polished = re.sub(pattern, replacement, polished)
        
        # Fix sentence capitalization after periods
        sentences = re.split(r'(\.\s+)', polished)
        fixed_sentences = []
        
        for i, part in enumerate(sentences):
            if i % 2 == 0 and part.strip():  # Actual sentence content
                if part and part[0].islower():
                    part = part[0].upper() + part[1:]
            fixed_sentences.append(part)
        
        return ''.join(fixed_sentences).strip()

    def _gemini_polish(self, text: str) -> Optional[str]:
        """Use Gemini to polish text while preserving anti-detection features"""
        if not self.gemini_available:
            return None
        
        prompt = f"""Polish the following text to improve fluency, coherence, and natural flow. 

CRITICAL REQUIREMENTS:
- Keep ALL filler phrases like "in some cases", "you might say", etc.
- Preserve ALL sentence length variations (short and long sentences)
- Maintain ALL informal word choices and synonym substitutions
- Keep ALL parenthetical comments and asides
- DO NOT make the text sound too formal or academic
- DO NOT remove any human-like imperfections or quirks
- Only fix obvious grammar errors and improve flow between sentences

Your goal is to make it read more naturally while keeping all the stylistic elements that make it human-like.

Text to polish:
{text}

Polished version:"""

        try:
            response = self.model.generate_content(prompt, generation_config={
                "temperature": 0.3,
                "max_output_tokens": 1000
            })
            
            polished = response.text.strip()
            
            # Basic validation - ensure we didn't lose too much content
            if len(polished.split()) < len(text.split()) * 0.8:
                logger.warning("Gemini polishing removed too much content, using rule-based fallback")
                return None
            
            return polished
            
        except Exception as e:
            logger.warning(f"⚠️ Gemini polishing failed: {e}")
            return None

    def polish(self, text: str, method: str = "auto") -> Dict[str, any]:
        """
        Polish text for improved fluency and coherence
        
        Args:
            text (str): Text to polish
            method (str): "auto", "gemini", or "rule_based"
            
        Returns:
            Dict with polished text and processing info
        """
        original_word_count = len(text.split())
        logger.info(f"🔧 Safe polishing with method: {method}")
        
        polished_text = text
        method_used = "none"
        
        if method == "auto":
            # Try Gemini first, fall back to rule-based
            if self.gemini_available:
                gemini_result = self._gemini_polish(text)
                if gemini_result:
                    polished_text = gemini_result
                    method_used = "gemini"
                else:
                    polished_text = self._rule_based_polish(text)
                    method_used = "rule_based"
            else:
                polished_text = self._rule_based_polish(text)
                method_used = "rule_based"
                
        elif method == "gemini" and self.gemini_available:
            gemini_result = self._gemini_polish(text)
            if gemini_result:
                polished_text = gemini_result
                method_used = "gemini"
            else:
                # Fallback to rule-based
                polished_text = self._rule_based_polish(text)
                method_used = "rule_based_fallback"
                
        elif method == "rule_based":
            polished_text = self._rule_based_polish(text)
            method_used = "rule_based"
        
        final_word_count = len(polished_text.split())
        
        logger.info(f"✅ Safe polishing complete ({method_used}): {original_word_count} → {final_word_count} words")
        
        return {
            "text": polished_text,
            "original_word_count": original_word_count,
            "final_word_count": final_word_count,
            "method_used": method_used,
            "word_count_change": final_word_count - original_word_count
        } 