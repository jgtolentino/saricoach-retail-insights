import psycopg
from datetime import date
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

                # 2. Fetch Daily Metrics (For Today)
                # Use Manila time for "Today"
                cur.execute("""
                    SELECT volume, revenue, avg_basket_size, avg_duration_seconds
                    FROM daily_metrics 
                    WHERE store_id = %s AND date = (now() at time zone 'Asia/Manila')::date
                """, (store_id,))
                metrics = cur.fetchone()
                
                if not metrics:
                    # Fallback empty state if no data for today
                    return StoreSummary(
                        store_id=store_id,
                        store_name=store_name,
                        period="No Data Today",
                        kpis=[],
                        chart=[],
                        insights=[],
                        coach_message="No data recorded yet."
                    )

                (vol, rev, basket, dur) = metrics

                # 3. Fetch Chart Data
                cur.execute("""
                    SELECT hour_of_day, volume 
                    FROM hourly_traffic 
                    WHERE store_id = %s AND date = (now() at time zone 'Asia/Manila')::date
                    ORDER BY hour_of_day ASC
                """, (store_id,))
                chart_rows = cur.fetchall()
                
                chart_data = [
                    {"date": f"{row[0]:02d}:00", "volume": row[1]} 
                    for row in chart_rows
                ]

                # 4. Fetch Insights
                cur.execute("""
                    SELECT insights, coach_message 
                    FROM daily_insights 
                    WHERE store_id = %s AND date = (now() at time zone 'Asia/Manila')::date
                """, (store_id,))
                insight_res = cur.fetchone()
                
                insights_list = insight_res[0] if insight_res else []
                coach_msg = insight_res[1] if insight_res else "Analysis pending..."

                # 5. Construct Response
                return StoreSummary(
                    store_id=store_id,
                    store_name=store_name,
                    period="Today",
                    kpis=[
                        Kpi(label="Daily Volume", value=vol, delta_pct=12.3, trend="up"), # Deltas hardcoded for demo, or calculate vs yesterday
                        Kpi(label="Daily Revenue", value=f"₱{rev:,.0f}", delta_pct=-5.1, trend="down"),
                        Kpi(label="Avg Basket", value=float(basket), delta_pct=2.0, trend="up"),
                        Kpi(label="Avg Duration", value=f"{dur}s", delta_pct=0.0, trend="neutral"),
                    ],
                    chart=chart_data,
                    insights=insights_list,
                    coach_message=coach_msg
                )
