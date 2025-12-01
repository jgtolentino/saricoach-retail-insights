"""Reset today's demo data in Supabase for store 1.

This script clears and re-inserts demo-friendly metrics, hourly traffic,
and insights for the current date so the dashboard always has fresh data.
"""

import os
from dataclasses import dataclass
from typing import List, Tuple

import psycopg
from dotenv import load_dotenv


@dataclass
class DemoConfig:
    store_id: int = 1
    daily_metrics: Tuple[int, float, float, int] = (649, 135_785.00, 2.4, 42)
    hourly_traffic: List[Tuple[int, int]] = None  # type: ignore[assignment]
    insights: List[str] = None  # type: ignore[assignment]
    coach_message: str = (
        "Revenue is strong (₱135k), but traffic is spiking late. "
        "Ensure staff is ready for the 6 PM rush."
    )

    def __post_init__(self) -> None:
        if self.hourly_traffic is None:
            self.hourly_traffic = [
                (8, 45),
                (10, 120),
                (12, 160),
                (14, 90),
                (16, 140),
                (18, 190),
            ]
        if self.insights is None:
            self.insights = [
                "Peak traffic detected at 6 PM.",
                "Inventory Alert: Coke Zero low.",
            ]


def get_db_url() -> str:
    """Load the database URL from the service/.env file."""
    load_dotenv("service/.env")
    db_url = os.getenv("SARICOACH_DATABASE_URL")
    if not db_url:
        raise RuntimeError("SARICOACH_DATABASE_URL not found in service/.env")
    return db_url


def reset_demo_data(config: DemoConfig) -> None:
    """Reset today's data for the configured store."""
    db_url = get_db_url()

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            print("🚀 Connecting to Supabase...")

            # Clean existing rows for the current date to avoid duplicates
            cur.execute(
                "DELETE FROM daily_metrics WHERE store_id = %s AND date = CURRENT_DATE",
                (config.store_id,),
            )
            cur.execute(
                "DELETE FROM hourly_traffic WHERE store_id = %s AND date = CURRENT_DATE",
                (config.store_id,),
            )
            cur.execute(
                "DELETE FROM daily_insights WHERE store_id = %s AND date = CURRENT_DATE",
                (config.store_id,),
            )

            volume, revenue, avg_basket, avg_duration = config.daily_metrics
            cur.execute(
                """
                INSERT INTO daily_metrics (store_id, date, volume, revenue, avg_basket_size, avg_duration_seconds)
                VALUES (%s, CURRENT_DATE, %s, %s, %s, %s)
                """,
                (config.store_id, volume, revenue, avg_basket, avg_duration),
            )

            cur.executemany(
                """
                INSERT INTO hourly_traffic (store_id, date, hour_of_day, volume)
                VALUES (%s, CURRENT_DATE, %s, %s)
                """,
                [(config.store_id, hour, vol) for hour, vol in config.hourly_traffic],
            )

            cur.execute(
                """
                INSERT INTO daily_insights (store_id, date, insights, coach_message)
                VALUES (%s, CURRENT_DATE, %s, %s)
                """,
                (config.store_id, config.insights, config.coach_message),
            )

        conn.commit()

    print("✅ SUCCESS: Real data injected for TODAY.")


def main() -> None:
    config = DemoConfig()
    reset_demo_data(config)


if __name__ == "__main__":
    main()
