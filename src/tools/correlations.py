from typing import Any, Dict
import pandas as pd


def summarize_overall(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute overall KPIs: daily volume, revenue, avg basket size."""
    if df.empty:
        return {
            "daily_volume": 0,
            "daily_revenue": 0.0,
            "avg_basket_size": 0.0,
        }

    # volume per day = distinct transactions per day
    tx_per_day = df.groupby("day")["transaction_id"].nunique()
    revenue_per_day = df.groupby("day")["subtotal"].sum()
    items_per_tx = df.groupby("transaction_id")["qty"].sum()

    return {
        "daily_volume": float(tx_per_day.mean()),
        "daily_revenue": float(revenue_per_day.mean()),
        "avg_basket_size": float(items_per_tx.mean()),
        "days_observed": int(tx_per_day.shape[0]),
    }


def summarize_by_brand(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Basic per-brand metrics."""
    if df.empty:
        return {}

    grouped = df.groupby("brand_id")
    res: Dict[str, Dict[str, Any]] = {}
    for brand_id, g in grouped:
        res[str(brand_id)] = {
            "volume": float(g["transaction_id"].nunique()),
            "revenue": float(g["subtotal"].sum()),
            "avg_qty": float(g["qty"].mean()),
        }
    return res
