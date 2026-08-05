"""
llm_config.py
--------------
Centralised LLM provider setup for the YouTube Content Planner.

Supports two backends, matching the "Suggested APIs / Tools" column
of the project spec:
    - Google Gemini  (langchain_google_genai)
    - Groq           (langchain_groq)

Switch providers either by:
    1. Setting LLM_PROVIDER in .env, or
    2. Passing provider="gemini" / "groq" explicitly to get_llm().
"""

import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
DEFAULT_GROQ_MODEL = "llama-3.1-70b-versatile"


class MissingAPIKeyError(RuntimeError):
    """Raised when the selected provider has no API key configured."""


def get_llm(provider: str | None = None, temperature: float = 0.7):
    """
    Return a configured LangChain chat model instance.

    Args:
        provider: "gemini" or "groq". Falls back to LLM_PROVIDER env var,
                  then defaults to "gemini".
        temperature: creativity control passed to the underlying model.
    """
    provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower().strip()

    if provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or "your_gemini_api_key_here" in api_key:
            raise MissingAPIKeyError(
                "GOOGLE_API_KEY is missing. Add it to your .env file. "
                "Get one at https://aistudio.google.com/app/apikey"
            )
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=DEFAULT_GEMINI_MODEL,
            google_api_key=api_key,
            temperature=temperature,
        )

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or "your_groq_api_key_here" in api_key:
            raise MissingAPIKeyError(
                "GROQ_API_KEY is missing. Add it to your .env file. "
                "Get one at https://console.groq.com/keys"
            )
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=DEFAULT_GROQ_MODEL,
            groq_api_key=api_key,
            temperature=temperature,
        )

    raise ValueError(f"Unknown provider '{provider}'. Use 'gemini' or 'groq'.")
