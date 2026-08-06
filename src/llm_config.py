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

# "gemini-flash-latest" is Google's officially maintained alias that always
# points at the current Flash model, so this won't 404 again when a
# specific dated model (e.g. gemini-1.5-flash) is eventually retired.
DEFAULT_GEMINI_MODEL = "gemini-flash-latest"

# llama-3.1-70b-versatile / llama-3.3-70b-versatile were deprecated by Groq;
# openai/gpt-oss-120b is their recommended current replacement.
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"


class MissingAPIKeyError(RuntimeError):
    """Raised when the selected provider has no API key configured."""


def get_llm(provider: str | None = None, temperature: float = 0.7, api_key: str | None = None):
    """
    Return a configured LangChain chat model instance.

    Args:
        provider: "gemini" or "groq". Falls back to LLM_PROVIDER env var,
                  then defaults to "gemini".
        temperature: creativity control passed to the underlying model.
        api_key: explicit key to use (e.g. typed into the Streamlit sidebar
                 at runtime). Takes priority over .env / Streamlit Secrets /
                 any other environment variable.
    """
    provider = (provider or os.getenv("LLM_PROVIDER", "gemini")).lower().strip()

    if provider == "gemini":
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key or "your_gemini_api_key_here" in key:
            raise MissingAPIKeyError(
                "No Gemini API key found. Enter one in the sidebar, or add "
                "GOOGLE_API_KEY to your .env / Streamlit Secrets. "
                "Get a key at https://aistudio.google.com/app/apikey"
            )
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL),
            google_api_key=key,
            temperature=temperature,
        )

    if provider == "groq":
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key or "your_groq_api_key_here" in key:
            raise MissingAPIKeyError(
                "No Groq API key found. Enter one in the sidebar, or add "
                "GROQ_API_KEY to your .env / Streamlit Secrets. "
                "Get a key at https://console.groq.com/keys"
            )
        from langchain_groq import ChatGroq

        return ChatGroq(
            model=os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL),
            groq_api_key=key,
            temperature=temperature,
        )

    raise ValueError(f"Unknown provider '{provider}'. Use 'gemini' or 'groq'.")
