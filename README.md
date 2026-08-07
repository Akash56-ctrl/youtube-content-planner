# 📺 YouTube Content Planner

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Chain-green)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

| Project ID | Level | Core Concept |
|---|---|---|
| MED-01 | Intermediate | LangChain **Chain** |

An AI-powered content planning assistant for YouTube creators. Give it your
channel niche and audience, and it runs a **4-stage LangChain sequential chain**
to produce a full content plan in one pass.

## ✨ Features

- 💡 **Video idea generation** — a batch of fresh video concepts for your niche
- 🔍 **SEO title suggestions** — each idea rewritten into a keyword-optimised title
- 🖼️ **Thumbnail suggestions** — text overlay, visual direction, and colour mood per video
- 🗓️ **Upload schedule** — dates assigned based on your posting frequency

## 🧠 How the chain works

This project intentionally uses a **Chain**, not an agent — each step's
output is deterministic input for the next step, with no autonomous
decision-making:

```
niche + audience + tone
        │
        ▼
 ┌─────────────────┐
 │  1. Video Ideas  │
 └─────────────────┘
        │
        ▼
 ┌─────────────────┐
 │  2. SEO Titles   │
 └─────────────────┘
        │
        ▼
 ┌───────────────────┐
 │ 3. Thumbnail Ideas │
 └───────────────────┘
        │
        ▼
 ┌───────────────────┐
 │ 4. Upload Schedule │
 └───────────────────┘
```

Implemented with LangChain Expression Language (LCEL) `RunnableSequence`s in
[`src/chains.py`](src/chains.py).

## 🔌 Supported APIs

| Provider | Package | Get a key |
|---|---|---|
| Google Gemini | `langchain-google-genai` | https://aistudio.google.com/app/apikey |
| Groq | `langchain-groq` | https://console.groq.com/keys |

Switch providers from the sidebar dropdown in the app, or set `LLM_PROVIDER`
in `.env`.

## 🚀 Getting started

```bash
# 1. Clone the repo
git clone https://github.com/Akash56-ctrl/YouTube-Content-Planner.git
cd YouTube-Content-Planner

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key(s)
cp .env.example .env
# then edit .env and paste in your GOOGLE_API_KEY and/or GROQ_API_KEY

# 5. Run the app
streamlit run app.py
```

## 📁 Project structure

```
YouTube-Content-Planner/
├── app.py                 # Streamlit UI
├── src/
│   ├── chains.py           # LangChain sequential chain wiring
│   ├── llm_config.py       # Gemini / Groq provider setup
│   └── prompts.py          # Prompt templates for each stage
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Tech stack

- Python
- LangChain (LCEL Chains)
- Streamlit
- Google Gemini API / Groq API
