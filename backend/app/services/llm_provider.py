"""LLM provider: calls OpenAI and tracks which guidelines were reflected."""

from openai import AsyncOpenAI

from app.config import settings
from app.schemas import Attribution

def _get_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=settings.openai_api_key)


async def ask_llm(
    system_prompt: str,
    question: str,
    guideline_records: list[dict],
) -> tuple[str, list[Attribution]]:
    """Send the question to the LLM and return (answer, attributions).

    Attribution is determined by checking which guideline texts are
    reflected in the response (simple substring heuristic for the demo).
    """
    response = await _get_client().chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=800,
    )

    answer = response.choices[0].message.content or ""

    # Simple attribution: check which guidelines likely influenced the response.
    # For each guideline, extract key phrases and check if the response
    # addresses the same topic.
    attributions = _find_attributions(answer, question, guideline_records)

    return answer, attributions


def _find_attributions(
    answer: str, question: str, guideline_records: list[dict]
) -> list[Attribution]:
    """Heuristic attribution: find which guidelines were relevant to the response."""
    answer_lower = answer.lower()
    question_lower = question.lower()
    attributed: list[Attribution] = []
    seen_texts: set[str] = set()

    for g in guideline_records:
        if g["voice_name"] == "Compass Defaults":
            continue  # don't attribute platform defaults

        text = g["guideline_text"].lower()
        keywords = _extract_keywords(text)

        # A guideline is attributed if its keywords appear in the question or answer
        question_match = sum(1 for k in keywords if k in question_lower)
        answer_match = sum(1 for k in keywords if k in answer_lower)

        if question_match >= 1 or answer_match >= 2:
            if g["guideline_text"] not in seen_texts:
                seen_texts.add(g["guideline_text"])
                attributed.append(
                    Attribution(
                        voice_name=g["voice_name"],
                        voice_icon=g["voice_icon"],
                        guideline_text=g["guideline_text"],
                    )
                )

    return attributed


def _extract_keywords(text: str) -> list[str]:
    """Pull meaningful words from a guideline for matching."""
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "about", "if", "or",
        "and", "but", "not", "no", "nor", "so", "yet", "she", "he", "her",
        "his", "it", "its", "they", "them", "their", "this", "that", "i",
    }
    words = text.split()
    return [w.strip(".,!?\"'()") for w in words if len(w) > 2 and w not in stop_words]
