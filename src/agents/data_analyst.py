from typing import Any, Dict

from src.tools import (
    get_store,
    get_transactions,
    build_feature_frame,
    summarize_overall,
    summarize_by_brand,
)


class DataAnalystAgent:
    """Turns payload into structured metrics."""

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        store = get_store(payload)
        _ = get_transactions(payload)  # not used directly, but validates
        df = build_feature_frame(payload)

        overall = summarize_overall(df)
        by_brand = summarize_by_brand(df)

        return {
            "store": {
                "id": store.get("id"),
                "name": store.get("name"),
                "code": store.get("code"),
                "region": store.get("region"),
                "city": store.get("city"),
            },
            "overall": overall,
            "brands": by_brand,
        }
