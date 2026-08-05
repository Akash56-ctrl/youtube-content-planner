"""
prompts.py
----------
All prompt templates used by the content-planning chain, kept separate
from chain wiring so they're easy to tune independently.
"""

from langchain_core.prompts import ChatPromptTemplate

IDEA_PROMPT = ChatPromptTemplate.from_template(
    """You are a YouTube content strategist for a channel in the "{niche}" niche.
The target audience is: {audience}
The desired tone/style is: {tone}

Generate exactly {num_ideas} distinct video ideas for this channel.
For each idea provide:
- A working title (not yet SEO-optimised)
- A one-sentence concept/hook describing what the video covers

Format your answer as a numbered list, one idea per line, like:
1. Working Title -- Concept sentence.
2. Working Title -- Concept sentence.
"""
)

SEO_TITLE_PROMPT = ChatPromptTemplate.from_template(
    """You are an SEO specialist for YouTube.
Below is a numbered list of raw video ideas for a channel in the
"{niche}" niche targeting: {audience}

{video_ideas}

For EACH numbered idea, rewrite it into an SEO-optimised YouTube title.
Rules:
- Keep each title under 60 characters where possible
- Front-load the main keyword
- Make it clickable but not misleading (no clickbait lies)
- Keep the same numbering as the input list

Return only the numbered list of optimised titles.
"""
)

THUMBNAIL_PROMPT = ChatPromptTemplate.from_template(
    """You are a YouTube thumbnail designer.
Here are the SEO-optimised titles for an upcoming batch of videos:

{seo_titles}

For EACH numbered title, suggest a thumbnail concept containing:
- Short bold text overlay (max 4 words)
- Visual/imagery direction (what should be shown)
- Suggested colour mood (e.g. high-contrast red/black, cool blue tech tones)

Keep the same numbering as the input list. Format each entry as:
1. Text: "..." | Visual: ... | Colours: ...
"""
)

SCHEDULE_PROMPT = ChatPromptTemplate.from_template(
    """You are a YouTube publishing strategist.
A creator uploads {upload_frequency} and wants to schedule the following
{num_ideas} videos, starting from {start_date}:

{seo_titles}

Create an upload schedule that:
- Assigns each video a specific date based on the frequency given
- Spreads content types sensibly (avoid two very similar topics back-to-back
  if the titles suggest similar subject matter)
- Notes the best day-of-week for this audience if relevant: {audience}

Return the schedule as a numbered list: Date -- Title.
"""
)
