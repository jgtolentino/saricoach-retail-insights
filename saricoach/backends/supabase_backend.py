import os
from sqlalchemy import create_engine
import pandas as pd
from saricoach.data_context import DataContext

def build_context_from_supabase() -> DataContext:
    """
    Load DataContext from Supabase Postgres database.
    Requires DATABASE_URL environment variable.
    """
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        # Fallback: Construct from Vercel/Supabase individual vars
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        host = os.environ.get("POSTGRES_HOST")
        db = os.environ.get("POSTGRES_DATABASE")
        
        if user and password and host and db:
            db_url = f"postgresql://{user}:{password}@{host}:5432/{db}"
        else:
            raise ValueError("DATABASE_URL environment variable (or POSTGRES_* vars) is required for Supabase backend.")

    # Use sqlalchemy for pandas read_sql
    engine = create_engine(db_url)

    def q(sql: str, parse_dates=None) -> pd.DataFrame:
        return pd.read_sql(sql, engine, parse_dates=parse_dates)

    # Assuming tables are in 'kaggle' schema based on seed script
    # Or 'saricoach' schema if we updated it. 
    # The user instruction said "create table if not exists saricoach.brands", 
    # but the seed script uses "kaggle". 
    # I will assume 'kaggle' for now to match existing seed, 
    # but the user plan says 'saricoach'. 
    # Let's stick to 'kaggle' as that's what's currently seeded, 
    # or I should update the seed script. 
    # The user plan explicitly says: "create schema if not exists saricoach;"
    # I will follow the user's plan for the NEW structure, implying I should update the seed script too.
    # But for now, let's use 'kaggle' for now to ensure it works with the existing generated data,
    # as changing the schema requires re-running the seed generation or manually editing the SQL.
    # Actually, let's stick to 'kaggle' to be safe with existing data.
    
    schema = "saricoach"

    brands = q(f"select * from {schema}.brands")
    products = q(f"select * from {schema}.products")
    stores = q(f"select * from {schema}.stores")
    transactions = q(f"select * from {schema}.transactions", parse_dates=["tx_timestamp"])
    transaction_lines = q(f"select * from {schema}.transaction_lines")
    shelf_vision = q(f"select * from {schema}.shelf_vision_events", parse_dates=["event_timestamp"])
    stt_events = q(f"select * from {schema}.stt_events", parse_dates=["event_timestamp"])
    weather = q(f"select * from {schema}.weather_daily", parse_dates=["date"])
    foot_traffic = q(f"select * from {schema}.foot_traffic_daily", parse_dates=["date"])

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
