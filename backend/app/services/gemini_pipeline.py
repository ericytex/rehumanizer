import time
import logging
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Generative AI not available. Install with: pip install google-generativeai")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Gemini model setup ---
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
if GEMINI_AVAILABLE and API_KEY != "YOUR_GEMINI_API_KEY" and API_KEY != "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro")
    print("✅ Gemini API configured for advanced pipeline")
else:
    model = None
    if not GEMINI_AVAILABLE:
        print("⚠️ Gemini API not available - install with: pip install google-generativeai")
    else:
        print("⚠️ Gemini API not configured - set GEMINI_API_KEY in .env file")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")

# --- Prompt Templates ---
PROMPTS = {
    "summarize": (
        "Pass 1 — Summarize the key points and intent of the following text in 2-3 concise sentences. "
        "This is for reference in later steps. Do not add introductions or extra commentary.\n\n"
        "TEXT:\n{original}\n\nSUMMARY (text only):"
    ),
    "add_specifics": (
        "Pass 2 — Expand the summary into a natural, human-sounding essay between 300 and 350 words. "
        "Use only the real details provided. Keep original meaning and tone. Do not add introductions or closing remarks; "
        "return only the essay text.\n\nSUMMARY:\n{summary}\n\nREAL DETAILS:\n{details}\n\nESSAY:"
    ),
    "vary_rhythm": (
        "Pass 3 — Rewrite for smoother rhythm and sentence variety while keeping length between 300 and 350 words. "
        "Avoid repetitive phrasing. Do not add intro or conclusion phrases. Return only the essay text.\n\n"
        "TEXT:\n{draft}\n\nREVISED ESSAY:"
    ),
    "proofread_tone": (
        "Pass 4 — Proofread for grammar, clarity, and cohesion. Keep length above 300 words. "
        "Do not add intros, conclusions, or explanations; return only the polished essay text.\n\n"
        "TEXT:\n{draft}\n\nFINAL ESSAY:"
    ),
    "humanize_ai_text": (
        "Transform this AI-generated text into natural, human-sounding content while maintaining the same length and core meaning. "
        "Make it conversational, add personal touches, vary sentence structure, and use casual language. "
        "Keep the core meaning but make it sound like a human wrote it. "
        "IMPORTANT: Maintain the same approximate word count as the original text. "
        "Return only the humanized text.\n\n"
        "AI TEXT:\n{text}\n\nHUMANIZED TEXT:"
    ),
    "expand_text": (
        "Expand the following text naturally so that it is at least {min_words} words. "
        "Add elaboration and detail but keep meaning and tone the same. "
        "Return only the expanded text.\n\nTEXT:\n{text}\n\nEXPANDED TEXT:"
    ),
    "add_personality": (
        "Add human personality and conversational elements to this text while maintaining the same length. "
        "Include casual phrases, personal opinions, and natural speech patterns. "
        "Make it sound like a real person wrote it. Return only the enhanced text.\n\n"
        "TEXT:\n{text}\n\nENHANCED TEXT:"
    ),
    "vary_sentence_structure": (
        "Rewrite this text with varied sentence structures - mix short and long sentences, "
        "use different sentence types (declarative, interrogative, exclamatory), and "
        "vary the rhythm while keeping the same meaning and length. Return only the rewritten text.\n\n"
        "TEXT:\n{text}\n\nREWRITTEN TEXT:"
    ),
}

# --- Helpers ---
def model_call_with_retry(client, prompt, temperature=0.4, max_tokens=600, retries=3):
    """Call the Gemini model with retry logic."""
    for attempt in range(retries):
        try:
            logger.info(f"Model call attempt {attempt + 1}")
            response = client.generate_content(prompt, generation_config={"temperature": temperature, "max_output_tokens": max_tokens})
            text = response.text.strip()
            return {"text": clean_text(text)}
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError("Model call failed after retries.")

def clean_text(text: str) -> str:
    """Remove intros, labels, and extra formatting from model output."""
    lines = text.strip().split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove common unwanted prefixes
        for prefix in ["FINAL:", "FINAL ESSAY:", "DRAFT:", "REVISED ESSAY:", "ESSAY:", "SUMMARY:", "Here is", "Here's", "Output:", "HUMANIZED TEXT:", "ENHANCED TEXT:", "REWRITTEN TEXT:", "EXPANDED TEXT:"]:
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
        cleaned_lines.append(line)
    return " ".join(cleaned_lines)

def enforce_min_length(text: str, min_words: int = 300, client: Optional[genai.GenerativeModel] = None) -> str:
    """Ensure text meets the minimum word count, expanding if necessary."""
    words = text.split()
    if len(words) >= min_words or not client:
        return text
    logger.warning(f"Text only {len(words)} words; expanding to at least {min_words} words.")
    prompt = PROMPTS["expand_text"].format(text=text, min_words=min_words)
    r = model_call_with_retry(client, prompt, temperature=0.5, max_tokens=600)
    return r["text"].strip()

# --- Pass Functions ---
def pass_summarize(client, original):
    print("📝 Pass 1: Summarizing key points...")
    return model_call_with_retry(client, PROMPTS["summarize"].format(original=original), temperature=0.3)

def pass_add_specifics(client, summary, details):
    print("📝 Pass 2: Adding specifics and expanding...")
    return model_call_with_retry(client, PROMPTS["add_specifics"].format(summary=summary, details=details), temperature=0.5)

def pass_vary_rhythm(client, draft):
    print("📝 Pass 3: Varying rhythm and sentence structure...")
    return model_call_with_retry(client, PROMPTS["vary_rhythm"].format(draft=draft), temperature=0.6)

def pass_proofread_tone(client, draft):
    print("📝 Pass 4: Proofreading and finalizing tone...")
    return model_call_with_retry(client, PROMPTS["proofread_tone"].format(draft=draft), temperature=0.4)

def pass_humanize_ai_text(client, text):
    print("🤖 Pass: Humanizing AI text...")
    return model_call_with_retry(client, PROMPTS["humanize_ai_text"].format(text=text), temperature=0.7, max_tokens=800)

def pass_add_personality(client, text):
    print("👤 Pass: Adding personality and conversational elements...")
    return model_call_with_retry(client, PROMPTS["add_personality"].format(text=text), temperature=0.6, max_tokens=600)

def pass_vary_sentence_structure(client, text):
    print("📝 Pass: Varying sentence structure...")
    return model_call_with_retry(client, PROMPTS["vary_sentence_structure"].format(text=text), temperature=0.5, max_tokens=600)

# --- Main Pipeline ---
def run_advanced_pipeline(original_text, details=""):
    """Run the advanced 4-pass pipeline for comprehensive text humanization."""
    client = model
    if not client:
        print("⚠️ Gemini not available for advanced pipeline")
        return original_text
        
    logger.info("🚀 Starting advanced 4-pass pipeline...")
    original_word_count = len(original_text.split())
    print(f"📊 Original text: {original_word_count} words")

    try:
        # Pass 1: Summarize
        p1 = pass_summarize(client, original_text)
        print(f"✅ Pass 1 complete: {len(p1['text'].split())} words")

        # Pass 2: Add specifics and expand
        p2 = pass_add_specifics(client, p1["text"], details)
        p2["text"] = enforce_min_length(p2["text"], min_words=300, client=client)
        print(f"✅ Pass 2 complete: {len(p2['text'].split())} words")

        # Pass 3: Vary rhythm
        p3 = pass_vary_rhythm(client, p2["text"])
        p3["text"] = enforce_min_length(p3["text"], min_words=300, client=client)
        print(f"✅ Pass 3 complete: {len(p3['text'].split())} words")

        # Pass 4: Proofread and finalize
        p4 = pass_proofread_tone(client, p3["text"])
        p4["text"] = enforce_min_length(p4["text"], min_words=300, client=client)
        print(f"✅ Pass 4 complete: {len(p4['text'].split())} words")

        final_word_count = len(p4["text"].split())
        print(f"🎉 Advanced pipeline complete! Final: {final_word_count} words (started with {original_word_count})")
        
        return p4["text"]
    except Exception as e:
        print(f"⚠️ Advanced pipeline failed due to API limits or error: {e}")
        print("🔄 Falling back to original text")
        return original_text

def run_quick_humanization_pipeline(original_text):
    """Run a quick 3-pass pipeline for faster humanization."""
    client = model
    if not client:
        print("⚠️ Gemini not available for quick pipeline")
        return original_text
        
    logger.info("🚀 Starting quick 3-pass pipeline...")
    original_word_count = len(original_text.split())
    print(f"📊 Original text: {original_word_count} words")

    try:
        # Pass 1: Humanize AI text
        p1 = pass_humanize_ai_text(client, original_text)
        print(f"✅ Pass 1 complete: {len(p1['text'].split())} words")

        # Pass 2: Add personality
        p2 = pass_add_personality(client, p1["text"])
        print(f"✅ Pass 2 complete: {len(p2['text'].split())} words")

        # Pass 3: Vary sentence structure
        p3 = pass_vary_sentence_structure(client, p2["text"])
        print(f"✅ Pass 3 complete: {len(p3['text'].split())} words")

        final_word_count = len(p3["text"].split())
        print(f"🎉 Quick pipeline complete! Final: {final_word_count} words (started with {original_word_count})")
        
        return p3["text"]
    except Exception as e:
        print(f"⚠️ Quick pipeline failed due to API limits or error: {e}")
        print("🔄 Falling back to original text")
        return original_text

# --- Example Usage ---
if __name__ == "__main__":
    original = """I have always been passionate about justice and advocacy. From a young age, I found myself drawn to situations where I could stand up for fairness..."""
    details = "Lifelong interest in law, volunteer work at local legal aid clinic, debate team captain, focus on human rights."

    print("=== Testing Advanced Pipeline ===")
    final_essay_advanced = run_advanced_pipeline(original, details)
    print("\n=== Advanced Pipeline Result ===")
    print(final_essay_advanced)
    
    print("\n=== Testing Quick Pipeline ===")
    final_essay_quick = run_quick_humanization_pipeline(original)
    print("\n=== Quick Pipeline Result ===")
    print(final_essay_quick) 