"""Quick script to list available Gemini embedding models."""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

print("=" * 60)
print("Available Embedding Models:")
print("=" * 60)

for model in genai.list_models():
    if "embed" in model.name.lower():
        print(f"\n  Name: {model.name}")
        print(f"  Display: {model.display_name}")
        print(f"  Methods: {model.supported_generation_methods}")

print("\n" + "=" * 60)
print("All Available Models:")
print("=" * 60)

for model in genai.list_models():
    print(f"  {model.name} — {model.supported_generation_methods}")
