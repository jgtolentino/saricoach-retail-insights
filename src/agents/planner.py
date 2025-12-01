from typing import Any, Dict

from src.config import Settings
from src.llm import GoogleLLMClient
from src.tools import validate_payload
from .data_analyst import DataAnalystAgent
from .coach import CoachAgent


class PlannerAgent:
    """High-level orchestrator.

    1. Validate payload.
    2. Ask DataAnalystAgent for structured metrics.
    3. Ask CoachAgent for natural-language advice.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        llm_client = GoogleLLMClient(
            api_key=settings.google_api_key,
            model_name=settings.google_model,
        )
        self.data_analyst = DataAnalystAgent()
        self.coach = CoachAgent(llm_client)

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        validate_payload(payload)
        analysis = self.data_analyst.run(payload)
        summary = self.coach.run(analysis)

        return {
            "summary": summary,
            "analysis": analysis,
            "recommendations": {
                "text": summary,
                "meta": {"source": "saricoach-v1"},
            },
        }
