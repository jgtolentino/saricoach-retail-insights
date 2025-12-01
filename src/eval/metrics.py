from typing import Dict, List


def keyword_coverage(output: str, expected_keywords: List[str]) -> float:
    output_lower = output.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in output_lower)
    if not expected_keywords:
        return 1.0
    return hits / len(expected_keywords)


def score_case(output: str, expected_keywords: List[str]) -> Dict[str, float]:
    return {
        "keyword_coverage": keyword_coverage(output, expected_keywords),
    }
