from __future__ import annotations
from typing import Optional, List
import pandas as pd
import numpy as np
from .data_context import DataContext

def _normalize_dates(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = df.copy()
    out[col] = pd.to_datetime(out[col])
    out["date"] = out[col].dt.date
    return out

def build_brand_day_frame(
    ctx: DataContext,
    store_id: int,
    start_date: Optional[pd.Timestamp] = None,
    end_date: Optional[pd.Timestamp] = None,
    focus_brand_ids: Optional[List[int]] = None,
) -> pd.DataFrame:
    """
    Build a per-store, per-day, per-brand feature frame combining:
    - Sales (quantity, revenue)
    - Shelf vision (facings, share_of_shelf, oos_flag)
    - STT demand (mentions, intent mix, avg sentiment)
    - Weather (temp, rainfall, condition)
    - Foot traffic (traffic_index)
    """

    # --- Transactions + lines ---
    tx = _normalize_dates(ctx.transactions, "tx_timestamp")
    tx = tx[tx["store_id"] == store_id]

    tl = ctx.transaction_lines.copy()
    tl = tl.merge(
        tx[["transaction_id", "date"]],
        on="transaction_id",
        how="inner",
    )

    sales_agg = (
        tl.groupby(["date", "brand_id"])
        .agg(
            qty_sold=("quantity", "sum"),
            revenue=("subtotal", "sum"),
        )
        .reset_index()
    )

    # --- Shelf vision ---
    sv = _normalize_dates(ctx.shelf_vision, "event_timestamp")
    sv = sv[sv["store_id"] == store_id]

    shelf_agg = (
        sv.groupby(["date", "brand_id"])
        .agg(
            facings=("facings", "mean"),
            share_of_shelf=("share_of_shelf", "mean"),
            oos_rate=("oos_flag", "mean"),
        )
        .reset_index()
    )

    # --- STT events ---
    stt = _normalize_dates(ctx.stt_events, "event_timestamp")
    stt = stt[stt["store_id"] == store_id]

    stt_agg = (
        stt.groupby(["date", "brand_id"])
        .agg(
            mention_count=("id", "count"),
            avg_sentiment=("sentiment_score", "mean"),
        )
        .reset_index()
    )

    # Intent distribution (wide)
    if not stt.empty:
        intent_counts = (
            stt.groupby(["date", "brand_id", "intent_label"])["id"]
            .count()
            .reset_index(name="intent_count")
        )
        intent_pivot = intent_counts.pivot_table(
            index=["date", "brand_id"],
            columns="intent_label",
            values="intent_count",
            fill_value=0,
        ).reset_index()
        intent_pivot.columns = [
            "date",
            "brand_id",
            *[f"intent_{c}" for c in intent_pivot.columns[2:]],
        ]
    else:
        intent_pivot = pd.DataFrame(columns=["date", "brand_id"])

    # --- Weather & traffic (per store/day) ---
    w = ctx.weather.copy()
    w["date"] = pd.to_datetime(w["date"]).dt.date
    w = w[w["store_id"] == store_id]

    t = ctx.foot_traffic.copy()
    t["date"] = pd.to_datetime(t["date"]).dt.date
    t = t[t["store_id"] == store_id]

    wt = w.merge(
        t[["store_id", "date", "traffic_index"]],
        on=["store_id", "date"],
        how="left",
    )

    # --- Combine all signals ---
    df = sales_agg.merge(shelf_agg, on=["date", "brand_id"], how="outer")
    df = df.merge(stt_agg, on=["date", "brand_id"], how="outer")
    if not intent_pivot.empty:
        df = df.merge(intent_pivot, on=["date", "brand_id"], how="outer")
    
    # Merge weather/traffic on date
    # Note: sales_agg etc have date, brand_id. wt has date.
    # We need to be careful with the merge.
    # The original code merged on date, but df has multiple rows per date (one per brand).
    # This is a left join from df to wt.
    
    df = df.merge(
        wt[["date", "temp_c", "rainfall_mm", "condition", "traffic_index"]],
        on="date",
        how="left",
    )

    # Attach brand meta (name + category)
    brands = ctx.brands.copy()
    df = df.merge(brands[["brand_id", "brand_name", "category"]], on="brand_id", how="left")

    # Filter date range if provided
    if start_date is not None:
        start_d = pd.to_datetime(start_date).date()
        df = df[df["date"] >= start_d]
    if end_date is not None:
        end_d = pd.to_datetime(end_date).date()
        df = df[df["date"] <= end_d]

    # Filter brands if provided
    if focus_brand_ids:
        df = df[df["brand_id"].isin(focus_brand_ids)]

    # Sort for readability
    df = df.sort_values(["date", "brand_id"]).reset_index(drop=True)

    # Fill NaNs in numeric cols with 0 for downstream ML/statistics
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(0)

    return df


def summarize_brand_window(
    feature_frame: pd.DataFrame,
    window_days: int = 30,
) -> pd.DataFrame:
    """
    Take a daily feature frame and aggregate to a rolling window summary
    per brand. This is the object the CoachAgent will typically see.
    """
    df = feature_frame.copy()
    if "date" not in df.columns:
        raise ValueError("feature_frame must contain a 'date' column")

    # For capstone simplicity: just aggregate over entire frame
    # Ensure brand_id exists (it should from build_brand_day_frame)
    if "brand_id" not in df.columns:
         raise ValueError("feature_frame must contain a 'brand_id' column")

    grouped = (
        df.groupby("brand_id")
        .agg(
            brand_name=("brand_name", "first"),
            category=("category", "first"),
            days_observed=("date", "nunique"),
            qty_sold_total=("qty_sold", "sum"),
            qty_sold_avg=("qty_sold", "mean"),
            revenue_total=("revenue", "sum"),
            revenue_avg=("revenue", "mean"),
            facings_avg=("facings", "mean"),
            share_of_shelf_avg=("share_of_shelf", "mean"),
            oos_rate_avg=("oos_rate", "mean"),
            mentions_total=("mention_count", "sum"),
            avg_sentiment=("avg_sentiment", "mean"),
            traffic_avg=("traffic_index", "mean"),
            temp_avg=("temp_c", "mean"),
            rainfall_avg=("rainfall_mm", "mean"),
        )
        .reset_index()
    )

    return grouped
