import os
import sys
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL")
ROUNDS = 2
MAX_ROUNDS = 4
DEFAULT_MODE = "normal"

# --- validation ---

if not MODEL:
    print("error: MODEL not set in .env (e.g. MODEL=anthropic/claude-sonnet-4-20250514)")
    print("see .env.example for options.")
    sys.exit(1)

# local providers (no key needed)
_LOCAL = {"ollama", "lmstudio", "llamacpp"}

# remote providers: map prefix to required env var
_KEY_MAP = {
    "anthropic": "ANTHROPIC_API_KEY",
    "gpt": "OPENAI_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "together_ai": "TOGETHERAI_API_KEY",
    "groq": "GROQ_API_KEY",
    "fireworks_ai": "FIREWORKS_API_KEY",
    "replicate": "REPLICATE_API_KEY",
    "huggingface": "HUGGINGFACE_API_KEY",
}

_provider = MODEL.split("/")[0] if "/" in MODEL else MODEL.split("-")[0]

if _provider not in _LOCAL:
    _expected_key = _KEY_MAP.get(_provider)
    if _expected_key and not os.getenv(_expected_key):
        print(f"error: {_expected_key} not set in .env (required for model '{MODEL}')")
        print("see .env.example for options.")
        sys.exit(1)
