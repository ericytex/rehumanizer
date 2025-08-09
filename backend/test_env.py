#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🧪 Testing Environment Variables")
print("=" * 40)

# Check if .env file exists
env_file_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"📁 .env file exists: {os.path.exists(env_file_path)}")

# Check GEMINI_API_KEY
gemini_key = os.getenv("GEMINI_API_KEY")
print(f"🔑 GEMINI_API_KEY: {gemini_key[:10]}..." if gemini_key and len(gemini_key) > 10 else f"🔑 GEMINI_API_KEY: {gemini_key}")

# Check other environment variables
debug = os.getenv("DEBUG")
log_level = os.getenv("LOG_LEVEL")
print(f"🐛 DEBUG: {debug}")
print(f"📝 LOG_LEVEL: {log_level}")

# Test if the key looks like a real API key
if gemini_key:
    if gemini_key.startswith("AIza"):
        print("✅ API key format looks correct (starts with AIza)")
    else:
        print("⚠️ API key format doesn't look like a real Gemini API key")
else:
    print("❌ No GEMINI_API_KEY found in environment")

print("=" * 40) 