from typing import Any, Dict

from src.llm import GoogleLLMClient


SYSTEM_PROMPT = (
    "You are SariCoach, an AI retail coach for sari-sari stores. "
    "You receive a JSON object with metrics about one store's sales. "
    "Explain what is happening and give 3–5 actionable recommendations "
    "in simple, conversational language. Do not use jargon."
)


class CoachAgent:
    def __init__(self, llm_client: GoogleLLMClient):
        self._llm = llm_client

    def run(self, analysis: Dict[str, Any]) -> str:
        text = (
            "Here is the analysis JSON for a store:\n\n"
            f"{analysis}\n\n"
            "Based on this, explain briefly what patterns you see and what the "
            "store owner should do next."
        )
        return self._llm.chat(SYSTEM_PROMPT, text)
