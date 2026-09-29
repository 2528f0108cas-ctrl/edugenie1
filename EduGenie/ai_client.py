import os
from functools import lru_cache
from google import genai
from google.genai import types

class AIUnavailable(RuntimeError):
    pass

@lru_cache(maxsize=1)
def _client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise AIUnavailable("Gemini is not configured. Add GEMINI_API_KEY to your .env file.")
    return genai.Client(api_key=key)

async def generate(prompt: str, *, json_mode: bool = False) -> str:
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    config = types.GenerateContentConfig(
        temperature=0.4,
        response_mime_type="application/json" if json_mode else "text/plain",
    )
    try:
        response = _client().models.generate_content(model=model, contents=prompt, config=config)
        text = response.text
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
    except AIUnavailable:
        raise
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed ({type(exc).__name__}). Check API key, model name, and network access.") from exc
