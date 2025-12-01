import psycopg
from typing import Optional
from .base import DataBackend
from ..models import StoreSummary, Kpi

class SupabaseBackend(DataBackend):
    def __init__(self, db_url: str):
        self.db_url = db_url

    def fetch_store_summary(self, store_id: int) -> Optional[StoreSummary]:
        # Connect to Supabase
        with psycopg.connect(self.db_url) as conn:
            with conn.cursor() as cur:

                # 1. Fetch Store Info
                cur.execute("SELECT name FROM stores WHERE id = %s", (store_id,))
                store_res = cur.fetchone()
                if not store_res:
                    return None
                store_name = store_res[0]

                # 2. Determine Latest Available Date (most recent data point)
                cur.execute(
                    """
                    SELECT date
                    FROM daily_metrics
                    WHERE store_id = %s
                    ORDER BY date DESC
                    LIMIT 1
                    """,
                    (store_id,),
                )
                latest_date_res = cur.fetchone()

                if not latest_date_res:
                    # Fallback empty state if no data exists yet
                    return StoreSummary(
                        store_id=store_id,
                        store_name=store_name,
                        period="No Data",
                        kpis=[],
                        chart=[],
                        insights=[],
                        coach_message="No data recorded yet."
                    )

                latest_date = latest_date_res[0]

                # 3. Fetch Daily Metrics for the Latest Date
                cur.execute(
                    """
                    SELECT volume, revenue, avg_basket_size, avg_duration_seconds
                    FROM daily_metrics
                    WHERE store_id = %s AND date = %s
                    """,
                    (store_id, latest_date),
                )
                metrics = cur.fetchone()

                if not metrics:
                    # Should not happen if latest_date is derived from daily_metrics,
                    # but handle defensively.
                    return StoreSummary(
                        store_id=store_id,
                        store_name=store_name,
                        period="No Data",
                        kpis=[],
                        chart=[],
                        insights=[],
                        coach_message="No data recorded yet."
                    )

                (vol, rev, basket, dur) = metrics

                # 4. Fetch Chart Data
                cur.execute(
                    """
                    SELECT hour_of_day, volume
                    FROM hourly_traffic
                    WHERE store_id = %s AND date = %s
                    ORDER BY hour_of_day ASC
                    """,
                    (store_id, latest_date),
                )
                chart_rows = cur.fetchall()

                chart_data = [
                    {"date": f"{row[0]:02d}:00", "volume": row[1]}
                    for row in chart_rows
                ]

                # 5. Fetch Insights
                cur.execute(
                    """
                    SELECT insights, coach_message
                    FROM daily_insights
                    WHERE store_id = %s AND date = %s
                    """,
                    (store_id, latest_date),
                )
                insight_res = cur.fetchone()

                insights_list = insight_res[0] if insight_res else []
                coach_msg = insight_res[1] if insight_res else "Analysis pending..."

                period_label = latest_date.strftime("%Y-%m-%d")

                # 6. Construct Response
                return StoreSummary(
                    store_id=store_id,
                    store_name=store_name,
                    period=f"Latest ({period_label})",
                    kpis=[
                        Kpi(label="Daily Volume", value=vol, delta_pct=12.3, trend="up"),  # Deltas hardcoded for demo
                        Kpi(label="Daily Revenue", value=f"₱{rev:,.0f}", delta_pct=-5.1, trend="down"),
                        Kpi(label="Avg Basket", value=float(basket), delta_pct=2.0, trend="up"),
                        Kpi(label="Avg Duration", value=f"{dur}s", delta_pct=0.0, trend="neutral"),
                    ],
                    chart=chart_data,
                    insights=insights_list,
                    coach_message=coach_msg
                )
