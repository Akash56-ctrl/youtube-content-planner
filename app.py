"""
app.py
------
Streamlit UI for the YouTube Content Planner (MED-01).

Level: Intermediate
Core concept: LangChain Sequential Chain
Features: video ideas, SEO titles, thumbnail suggestions, upload schedule
APIs: Google Gemini / Groq
"""

import datetime
import streamlit as st

from src.chains import build_content_planner_chain
from src.llm_config import MissingAPIKeyError

st.set_page_config(
    page_title="YouTube Content Planner",
    page_icon="📺",
    layout="wide",
)

st.title("📺 YouTube Content Planner")
st.caption(
    "LangChain sequential chain: video ideas → SEO titles → thumbnail "
    "suggestions → upload schedule."
)

with st.sidebar:
    st.header("⚙️ Settings")
    provider = st.selectbox("LLM Provider", ["gemini", "groq"], index=0)
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7, 0.05)

    st.markdown("---")
    st.subheader("🔑 API Key")
    st.caption(
        "Paste your key here to use the app immediately — it's kept only "
        "in this browser session and is never saved to the repo or disk. "
        "Leave blank to fall back to a key set in `.env` / Streamlit Secrets."
    )

    if provider == "gemini":
        user_api_key = st.text_input(
            "Gemini API key",
            type="password",
            placeholder="AIza...",
            help="Get one at https://aistudio.google.com/app/apikey",
        )
    else:
        user_api_key = st.text_input(
            "Groq API key",
            type="password",
            placeholder="gsk_...",
            help="Get one at https://console.groq.com/keys",
        )

st.subheader("1. Tell us about your channel")

col1, col2 = st.columns(2)
with col1:
    niche = st.text_input("Channel niche / topic", placeholder="e.g. Personal Finance for Students")
    audience = st.text_input("Target audience", placeholder="e.g. college students in their early 20s")
with col2:
    tone = st.text_input("Tone / style", placeholder="e.g. casual, energetic, beginner-friendly")
    num_ideas = st.number_input("Number of video ideas", min_value=1, max_value=15, value=5)

st.subheader("2. Upload schedule preferences")
col3, col4 = st.columns(2)
with col3:
    upload_frequency = st.selectbox(
        "Upload frequency", ["once a week", "twice a week", "daily", "biweekly", "monthly"]
    )
with col4:
    start_date = st.date_input("Schedule start date", datetime.date.today())

generate = st.button("🚀 Generate Content Plan", type="primary", use_container_width=True)

if generate:
    if not niche or not audience:
        st.warning("Please fill in at least the niche and target audience.")
    else:
        with st.spinner("Running the content planning chain..."):
            try:
                chain = build_content_planner_chain(
                    provider=provider,
                    temperature=temperature,
                    api_key=user_api_key or None,
                )
                result = chain.invoke(
                    {
                        "niche": niche,
                        "audience": audience,
                        "tone": tone or "neutral",
                        "num_ideas": int(num_ideas),
                        "upload_frequency": upload_frequency,
                        "start_date": start_date.strftime("%Y-%m-%d"),
                    }
                )
            except MissingAPIKeyError as e:
                st.error(str(e))
                st.stop()
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        tab1, tab2, tab3, tab4 = st.tabs(
            ["💡 Video Ideas", "🔍 SEO Titles", "🖼️ Thumbnails", "🗓️ Upload Schedule"]
        )
        with tab1:
            st.markdown(result["video_ideas"])
        with tab2:
            st.markdown(result["seo_titles"])
        with tab3:
            st.markdown(result["thumbnails"])
        with tab4:
            st.markdown(result["schedule"])

        st.success("Content plan generated successfully.")

        full_plan = (
            f"# YouTube Content Plan\n\n"
            f"## Video Ideas\n{result['video_ideas']}\n\n"
            f"## SEO Titles\n{result['seo_titles']}\n\n"
            f"## Thumbnail Suggestions\n{result['thumbnails']}\n\n"
            f"## Upload Schedule\n{result['schedule']}\n"
        )
        st.download_button(
            "⬇️ Download full plan (Markdown)",
            data=full_plan,
            file_name="youtube_content_plan.md",
            mime="text/markdown",
        )
