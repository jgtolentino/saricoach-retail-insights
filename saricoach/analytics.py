from typing import Dict, Any
from saricoach.eval.types import AnalyticsResult

def compute_store_kpis(analytics: AnalyticsResult, store_id: int) -> Dict[str, Any]:
    """
    Compute high-level store KPIs from the analytics result.
    """
    # This logic was previously in service/app/main.py
    
    # Daily Sales (sum of today's sales across all brands)
    # We need to find "today" or the last day in the feature frame
    ff = analytics.feature_frame
    if ff.empty:
        return {
            "daily_sales": 0.0,
            "daily_sales_delta": 0.0,
            "stockout_risk": "unknown",
            "hot_brand": None,
        }

    last_date = ff["date"].max()
    today_df = ff[ff["date"] == last_date]
    
    today_sales = today_df["revenue"].sum()

    # Delta vs previous day
    prev_date = last_date - pd.Timedelta(days=1)
    prev_df = ff[ff["date"] == prev_date]
    prev_sales = prev_df["revenue"].sum() if not prev_df.empty else 0.0

    if prev_sales > 0:
        delta = (today_sales - prev_sales) / prev_sales
    else:
        delta = 0.0

    # Stockout Risk
    brand_summary = analytics.brand_summary
    if not brand_summary.empty and "oos_rate_avg" in brand_summary.columns:
        max_oos = brand_summary["oos_rate_avg"].max()
        if max_oos > 0.2:
            stockout_risk = "high"
        elif max_oos > 0.05:
            stockout_risk = "medium"
        else:
            stockout_risk = "low"
    else:
        stockout_risk = "low"

    # Hot Brand (top revenue)
    if not brand_summary.empty:
        top_brand = brand_summary.sort_values("revenue_total", ascending=False).iloc[0]
        hot_brand = top_brand["brand_name"]
    else:
        hot_brand = None

    return {
        "daily_sales": float(today_sales),
        "daily_sales_delta": float(round(delta, 3)),
        "stockout_risk": stockout_risk,
        "hot_brand": hot_brand,
    }

import pandas as pd
