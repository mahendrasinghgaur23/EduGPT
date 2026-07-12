import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# ─────────────────────────────────────────────
# Environment Variables
# ─────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_COLLECTION_NAME = os.getenv("ASTRA_DB_COLLECTION_NAME", "edugpt_docs")

# ─────────────────────────────────────────────
# Model Configuration
# ─────────────────────────────────────────────
# LLM: Groq (free, fast) — uses Llama models
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Embeddings: Google Gemini (still free — embedding quota is separate from LLM quota)
MAX_RETRIES = 3
RETRY_DELAY = 30


def validate_config():
    """Validate that all required environment variables are set."""
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not ASTRA_DB_API_ENDPOINT:
        missing.append("ASTRA_DB_API_ENDPOINT")
    if not ASTRA_DB_APPLICATION_TOKEN:
        missing.append("ASTRA_DB_APPLICATION_TOKEN")
    return missing


def get_llm(temperature=0.7):
    """Initialize and return the Groq LLM (Llama 3.3 70B)."""
    from langchain_groq import ChatGroq

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature,
        groq_api_key=GROQ_API_KEY,
        max_retries=MAX_RETRIES,
    )


def get_embeddings():
    """Initialize and return the Gemini Embeddings model (separate free quota)."""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )


def call_with_retry(chain, inputs, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """
    Call an LLM chain with automatic retry on rate limit (429) errors.
    Waits between retries to let the quota reset.
    """
    for attempt in range(max_retries):
        try:
            result = chain.run(**inputs)
            return result
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                if attempt < max_retries - 1:
                    wait_time = delay * (attempt + 1)
                    print(f"⏳ Rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    raise Exception(
                        f"Rate limit exceeded after {max_retries} retries. "
                        f"Please wait a few minutes and try again."
                    )
            else:
                raise
