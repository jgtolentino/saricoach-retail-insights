import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv("service/.env")
api_key = os.getenv("SARICOACH_GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"Key: {api_key[:5]}...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
