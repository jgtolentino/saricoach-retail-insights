from pathlib import Path
import pandas as pd
from saricoach.data_context import DataContext

def build_context_from_csv(data_dir: Path) -> DataContext:
    """
    Load DataContext from a directory of CSV files.
    """
    # Helper to read CSV safely
    def read(name: str, parse_dates=None) -> pd.DataFrame:
        p = data_dir / name
        if not p.exists():
            # Return empty DF with minimal columns if file missing?
            # Or raise error. For now, raise error as these are expected.
            raise FileNotFoundError(f"Missing required data file: {p}")
        return pd.read_csv(p, parse_dates=parse_dates)

    brands = read("brands.csv")
    products = read("products.csv")
    stores = read("stores.csv")
    transactions = read("transactions.csv", parse_dates=["tx_timestamp"])
    transaction_lines = read("transaction_lines.csv")
    shelf_vision = read("shelf_vision_events.csv", parse_dates=["event_timestamp"])
    stt_events = read("stt_events.csv", parse_dates=["event_timestamp"])
    weather = read("weather_daily.csv", parse_dates=["date"])
    foot_traffic = read("foot_traffic_daily.csv", parse_dates=["date"])

    return DataContext(
        brands=brands,
        products=products,
        stores=stores,
        transactions=transactions,
        transaction_lines=transaction_lines,
        shelf_vision=shelf_vision,
        stt_events=stt_events,
        weather=weather,
        foot_traffic=foot_traffic,
    )
