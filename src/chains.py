"""
chains.py
---------
Core LangChain "Chain" logic for the YouTube Content Planner.

This is a 4-stage SEQUENTIAL CHAIN (LCEL RunnableSequence style):

    video ideas  -->  SEO titles  -->  thumbnail suggestions  -->  upload schedule

Each stage's output is fed as context into the next stage's prompt,
which is the defining trait of the LangChain "Chain" pattern (as opposed
to an autonomous agent that decides its own steps/tools).
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.llm_config import get_llm
from src.prompts import (
    IDEA_PROMPT,
    SEO_TITLE_PROMPT,
    THUMBNAIL_PROMPT,
    SCHEDULE_PROMPT,
)


def build_content_planner_chain(provider: str | None = None, temperature: float = 0.7):
    """
    Assemble and return the full sequential chain.

    The returned Runnable expects a dict with keys:
        niche, audience, tone, num_ideas, upload_frequency, start_date

    And returns a dict with keys:
        video_ideas, seo_titles, thumbnails, schedule
    """
    llm = get_llm(provider=provider, temperature=temperature)
    parser = StrOutputParser()

    # Stage 1: raw video ideas
    idea_stage = IDEA_PROMPT | llm | parser

    # Stage 2: SEO titles, needs stage 1 output plus original inputs
    seo_stage = SEO_TITLE_PROMPT | llm | parser

    # Stage 3: thumbnail suggestions, needs stage 2 output
    thumbnail_stage = THUMBNAIL_PROMPT | llm | parser

    # Stage 4: upload schedule, needs stage 2 output plus scheduling inputs
    schedule_stage = SCHEDULE_PROMPT | llm | parser

    def run(inputs: dict) -> dict:
        video_ideas = idea_stage.invoke(
            {
                "niche": inputs["niche"],
                "audience": inputs["audience"],
                "tone": inputs["tone"],
                "num_ideas": inputs["num_ideas"],
            }
        )

        seo_titles = seo_stage.invoke(
            {
                "niche": inputs["niche"],
                "audience": inputs["audience"],
                "video_ideas": video_ideas,
            }
        )

        thumbnails = thumbnail_stage.invoke({"seo_titles": seo_titles})

        schedule = schedule_stage.invoke(
            {
                "upload_frequency": inputs["upload_frequency"],
                "num_ideas": inputs["num_ideas"],
                "start_date": inputs["start_date"],
                "seo_titles": seo_titles,
                "audience": inputs["audience"],
            }
        )

        return {
            "video_ideas": video_ideas,
            "seo_titles": seo_titles,
            "thumbnails": thumbnails,
            "schedule": schedule,
        }

    # Wrapped as a Runnable so it composes like any other LangChain chain
    return RunnablePassthrough() | run
