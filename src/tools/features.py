from typing import Any, Dict, List
import pandas as pd


def build_feature_frame(payload: Dict[str, Any]) -> pd.DataFrame:
    """Flatten transactions into a row-per-line DataFrame.

    Expected payload shape:
    {
      "store": {...},
      "transactions": [
        {
          "id": ...,
          "date": "2025-09-01T00:00:00",
          "total_amount": float,
          "lines": [
            {
              "product_id": int,
              "brand_id": int,
              "quantity": float,
              "price_unit": float,
              "subtotal": float,
            }, ...
          ],
        }, ...
      ]
    }
    """
    txs: List[Dict[str, Any]] = payload.get("transactions", [])
    rows = []
    for tx in txs:
        tx_date = pd.to_datetime(tx.get("date"))
        for line in tx.get("lines", []):
            rows.append(
                {
                    "transaction_id": tx.get("id"),
                    "date": tx_date,
                    "day": tx_date.normalize(),
                    "brand_id": line.get("brand_id"),
                    "product_id": line.get("product_id"),
                    "qty": float(line.get("quantity", 0.0)),
                    "price_unit": float(line.get("price_unit", 0.0)),
                    "subtotal": float(line.get("subtotal", 0.0)),
                }
            )

    if not rows:
        return pd.DataFrame(
            columns=[
                "transaction_id",
                "date",
                "day",
                "brand_id",
                "product_id",
                "qty",
                "price_unit",
                "subtotal",
            ]
        )

    df = pd.DataFrame(rows)
    return df
