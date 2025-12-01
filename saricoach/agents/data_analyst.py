import pandas as pd
import numpy as np
from saricoach.data_context import DataContext
from saricoach.feature_frame import build_brand_day_frame, summarize_brand_window
from saricoach.eval.types import PlannerDecision, AnalyticsResult

class DataAnalystAgent:
    """
    Data-facing agent.
    Responsibilities:
      - Build feature frame (store × day × brand).
      - Aggregate into brand-level summaries for the window.
      - Compute simple "risk" and "opportunity" signals.
    """

    def __init__(self, ctx: DataContext):
        self.ctx = ctx

    def analyze(self, decision: PlannerDecision) -> AnalyticsResult:
        # For now we keep date range implicit (all available)
        ff = build_brand_day_frame(self.ctx, store_id=decision.store_id)

        # Optional brand/category filtering
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
        Add "risk" and "opportunity" flags based on simple heuristics.
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
