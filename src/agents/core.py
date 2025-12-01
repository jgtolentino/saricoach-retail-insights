# src/agents/core.py

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Literal, Optional

import numpy as np
import pandas as pd

from src.feature_frame import DataContext, build_brand_day_frame, summarize_brand_window


FlowType = Literal[
    "analyze_store",
    "explain_brand",
    "seven_day_plan",
]


@dataclass
class PlannerDecision:
    flow: FlowType
    store_id: int
    brand_id: Optional[int] = None
    category: Optional[str] = None
    focus_days: int = 30


class PlannerAgent:
    """
    High-level "router" that decides which flow to execute based on
    a simple user query structure (for the capstone we keep this explicit).

    In the notebook you can bypass NLP and call this directly with
    known parameters (store_id, flow, etc.).
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


@dataclass
class AnalyticsResult:
    store_id: int
    decision: PlannerDecision
    feature_frame: pd.DataFrame
    brand_summary: pd.DataFrame


class DataAnalystAgent:
    """
    Data-facing agent.

    Responsibilities:
      - Build feature frame (store × day × brand).
      - Aggregate into brand-level summaries for the window.
      - Compute simple "risk" and "opportunity" signals (e.g. low facings,
        high demand, high oos).
    """

    def __init__(self, ctx: DataContext):
        self.ctx = ctx

    def analyze(self, decision: PlannerDecision) -> AnalyticsResult:
        # For now we keep date range implicit (all available) – already filtered upstream via seed.
        ff = build_brand_day_frame(self.ctx, store_id=decision.store_id)

        # Optional brand/category filtering for explain_brand / seven_day_plan
        if decision.brand_id is not None:
            ff = ff[ff["brand_id"] == decision.brand_id]

        if decision.category:
            ff = ff[ff["category"] == decision.category]

        brand_summary = summarize_brand_window(ff, window_days=decision.focus_days)
        brand_summary = self._add_simple_scores(brand_summary)

        return AnalyticsResult(
            store_id=decision.store_id,
            decision=decision,
            feature_frame=ff,
            brand_summary=brand_summary,
        )

    @staticmethod
    def _add_simple_scores(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add "risk" and "opportunity" flags based on simple heuristics:

          - risk_stockout: low facings + high mentions + non-zero oos_rate
          - risk_visibility: low share_of_shelf_avg vs category avg
          - opp_high_demand: high mentions, good sentiment, decent traffic
        """
        out = df.copy()

        # Category-level benchmarks
        cat_stats = (
            out.groupby("category")[["share_of_shelf_avg", "facings_avg"]]
            .mean()
            .rename(columns={
                "share_of_shelf_avg": "cat_share_avg",
                "facings_avg": "cat_facings_avg",
            })
        )
        out = out.merge(cat_stats, on="category", how="left")

        # Risk: potential stockout
        out["risk_stockout_score"] = np.where(
            (out["oos_rate_avg"] > 0.05) & (out["mentions_total"] > 0) & (out["facings_avg"] < out["cat_facings_avg"]),
            1.0,
            0.0,
        )

        # Risk: low visibility
        out["risk_visibility_score"] = np.where(
            out["share_of_shelf_avg"] < 0.5 * out["cat_share_avg"],
            1.0,
            0.0,
        )

        # Opportunity: strong demand + sentiment + traffic
        out["opp_high_demand_score"] = np.where(
            (out["mentions_total"] > out["mentions_total"].median()) &
            (out["avg_sentiment"] > 0) &
            (out["traffic_avg"] > out["traffic_avg"].median()),
            1.0,
            0.0,
        )

        return out


@dataclass
class CoachOutput:
    """
    Structured output for the CoachAgent.
    """
    actions: List[str]
    risks: List[str]
    opportunities: List[str]
    debug_notes: Dict[str, Any]


class CoachAgent:
    """
    Language-facing coaching agent.

    For Kaggle, we keep it deterministic and lightweight:
      - Build recommendations from heuristic scores and metrics.
      - Optionally, you can swap the text generation logic with Gemini (e.g. Gemini 3 / Flash 2.0)
        in a single method for advanced reasoning and cultural nuance.
    """

    def __init__(self, model_name: str = "heuristic", use_gemini: bool = False):
        self.model_name = model_name
        self.use_gemini = use_gemini
        # NOTE: do NOT hard-code API keys here for Kaggle.
        # If you wire Gemini, read os.environ["GEMINI_API_KEY"] in the notebook, not in repo.

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
            # Optional: call out to Gemini for richer text, using bs.to_dict(orient="records")
            # For the capstone you can leave this as a stub and just document how it would work.
            pass

        actions = []
        risks = []
        opps = []

        # Simple heuristics to keep it transparent for judges
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

        # Fallbacks if nothing triggered
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
            actions=dedupe_keep_order(actions),
            risks=dedupe_keep_order(risks),
            opportunities=dedupe_keep_order(opps),
            debug_notes=debug_notes,
        )


def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for x in items:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out
