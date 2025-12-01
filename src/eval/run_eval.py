import json
from pathlib import Path
from typing import Any, Dict

from src.config import Settings
from src.agents import PlannerAgent
from .metrics import score_case


def run_eval() -> None:
    settings = Settings()
    planner = PlannerAgent(settings=settings)

    scenarios_path = Path(__file__).with_name("scenarios_eval.jsonl")
    scores = []

    with scenarios_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            case: Dict[str, Any] = json.loads(line)
            payload = case["payload"]
            expected_keywords = case.get("expected_keywords", [])

            result = planner.run(payload)
            summary = result["summary"]

            s = score_case(summary, expected_keywords)
            scores.append(s)
            print(case["id"], s)

    if scores:
        avg_keyword_coverage = sum(s["keyword_coverage"] for s in scores) / len(scores)
        print("\nAverage keyword coverage:", round(avg_keyword_coverage, 3))


if __name__ == "__main__":
    run_eval()
