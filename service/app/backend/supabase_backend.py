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

                # 3. Fetch Daily Metrics for the Latest 2 Days (for Deltas)
                cur.execute(
                    """
                    SELECT date, volume, revenue, avg_basket_size, avg_duration_seconds
                    FROM daily_metrics
                    WHERE store_id = %s
                    ORDER BY date DESC
                    LIMIT 2
                    """,
                    (store_id,),
                )
                rows = cur.fetchall()

                if not rows:
                    return StoreSummary(
                        store_id=store_id,
                        store_name=store_name,
                        period="No Data",
                        kpis=[],
                        chart=[],
                        insights=[],
                        coach_message="No data recorded yet."
                    )

                # Current Day (Latest)
                curr = rows[0]
                curr_vol, curr_rev, curr_basket, curr_dur = curr[1], curr[2], curr[3], curr[4]

                # Previous Day (for Deltas)
                if len(rows) > 1:
                    prev = rows[1]
                    prev_vol, prev_rev, prev_basket, prev_dur = prev[1], prev[2], prev[3], prev[4]
                    
                    def calc_delta(curr, prev):
                        if not prev or prev == 0: return 0.0
                        return ((float(curr) - float(prev)) / float(prev)) * 100.0

                    d_vol = calc_delta(curr_vol, prev_vol)
                    d_rev = calc_delta(curr_rev, prev_rev)
                    d_basket = calc_delta(curr_basket, prev_basket)
                    d_dur = calc_delta(curr_dur, prev_dur)
                else:
                    d_vol = d_rev = d_basket = d_dur = 0.0

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
                        Kpi(label="Daily Volume", value=curr_vol, delta_pct=round(d_vol, 1), trend="up" if d_vol >= 0 else "down"),
                        Kpi(label="Daily Revenue", value=f"₱{curr_rev:,.0f}", delta_pct=round(d_rev, 1), trend="up" if d_rev >= 0 else "down"),
                        Kpi(label="Avg Basket", value=float(curr_basket), delta_pct=round(d_basket, 1), trend="up" if d_basket >= 0 else "down"),
                        Kpi(label="Avg Duration", value=f"{curr_dur}s", delta_pct=round(d_dur, 1), trend="up" if d_dur >= 0 else "down"),
                    ],
                    chart=chart_data,
                    insights=insights_list,
                    coach_message=coach_msg
                )
