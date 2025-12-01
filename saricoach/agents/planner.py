from typing import Dict, Any
from saricoach.eval.types import PlannerDecision

class PlannerAgent:
    """
    High-level "router" that decides which flow to execute based on
    a simple user query structure.
    """

    def plan(
        self,
        query: Dict[str, Any],
    ) -> PlannerDecision:
        """
        query example shapes:
          - {"type": "analyze_store", "store_id": 1, "days": 30}
          - {"type": "explain_brand", "store_id": 1, "brand_id": 10, "days": 30}
          - {"type": "seven_day_plan", "store_id": 1, "category": "Beverages", "days": 30}
        """
        flow_type = query.get("type", "analyze_store")
        store_id = int(query["store_id"])
        days = int(query.get("days", 30))
        brand_id = query.get("brand_id")
        category = query.get("category")

        if flow_type not in ("analyze_store", "explain_brand", "seven_day_plan"):
            flow_type = "analyze_store"

        return PlannerDecision(
            flow=flow_type, store_id=store_id,
            brand_id=brand_id, category=category,
            focus_days=days,
        )
