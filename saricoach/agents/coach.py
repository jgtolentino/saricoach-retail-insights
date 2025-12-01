from typing import Literal, List
from saricoach.eval.types import AnalyticsResult, CoachOutput

class CoachAgent:
    """
    Language-facing coaching agent.
    """

    def __init__(self, model_name: str = "heuristic", use_gemini: bool = False):
        self.model_name = model_name
        self.use_gemini = use_gemini

    def coach(
        self,
        analytics: AnalyticsResult,
        persona: Literal["store_owner", "brand_manager", "distributor"] = "store_owner",
    ) -> CoachOutput:
        """
        Turn AnalyticsResult.brand_summary into human-readable next steps.
        """
        bs = analytics.brand_summary.copy()

        if self.use_gemini and self.model_name != "heuristic":
            # Optional: call out to Gemini for richer text
            pass

        actions = []
        risks = []
        opps = []

        # Simple heuristics
        for _, row in bs.iterrows():
            brand = row["brand_name"]
            cat = row["category"]

            # Risk: stockout
            if row.get("risk_stockout_score", 0) > 0:
                risks.append(
                    f"{brand} ({cat}) is at risk of stockout: low facings and some days out-of-stock despite demand."
                )
                actions.append(
                    f"Increase {brand} facings and ensure safety stock for the next 7 days, especially on peak days."
                )

            # Risk: visibility
            if row.get("risk_visibility_score", 0) > 0:
                risks.append(
                    f"{brand} ({cat}) has low share of shelf vs other brands in the same category."
                )
                actions.append(
                    f"Rearrange the shelf to give {brand} more eye-level space or move it closer to the counter."
                )

            # Opportunity: high demand
            if row.get("opp_high_demand_score", 0) > 0:
                opps.append(
                    f"{brand} ({cat}) shows strong demand and positive sentiment when traffic is high."
                )
                actions.append(
                    f"Highlight {brand} with small in-store signage or bundles, especially on weekends and paydays."
                )

        # Fallbacks
        if not actions:
            actions.append(
                "Maintain current assortment and monitor daily sales; no urgent changes detected for the next 7 days."
            )
        if not risks:
            risks.append("No critical risks detected based on the last observation window.")
        if not opps:
            opps.append("Look for opportunities to test small promos on top-selling brands during high-traffic days.")

        debug_notes = {
            "num_brands": len(bs),
            "store_id": analytics.store_id,
            "flow": analytics.decision.flow,
        }

        return CoachOutput(
            actions=self._dedupe_keep_order(actions),
            risks=self._dedupe_keep_order(risks),
            opportunities=self._dedupe_keep_order(opps),
            debug_notes=debug_notes,
        )

    @staticmethod
    def _dedupe_keep_order(items: List[str]) -> List[str]:
        seen = set()
        out: List[str] = []
        for x in items:
            if x in seen:
                continue
            seen.add(x)
            out.append(x)
        return out
