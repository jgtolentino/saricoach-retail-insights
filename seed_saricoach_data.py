#!/usr/bin/env python3
"""
Seed generator for SariCoach / Sari-Sari Expert.

- Ingests Kaggle-style raw datasets (store sales + baskets).
- Normalizes to canonical SariCoach schema:
  - brands, products, stores
  - transactions, transaction_lines
  - shelf_vision_events, stt_events, weather_daily, foot_traffic_daily
- Exports:
  - CSVs under data/processed/
  - Optional Postgres INSERT SQL under data/processed/seed_saricoach.sql

Customize:
- load_raw_kaggle_data()
- mappings in build_dim_* functions to match your chosen Kaggle datasets.
"""

import os
from pathlib import Path
import uuid
import random
from datetime import datetime, timedelta

import pandas as pd
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUT_DIR = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ---------------------------------------------------------------------------
# 0. Canonical schema definitions (for reference)
# ---------------------------------------------------------------------------
# brands:
#   brand_id (int), brand_name (str), category (str)
#
# products:
#   product_id (int), sku (str), barcode (str), brand_id (int),
#   product_name (str), category (str), pack_size (str), pack_type (str)
#
# stores:
#   store_id (int), store_name (str), region (str),
#   city (str), barangay (str), store_type (str)
#
# transactions:
#   transaction_id (str), store_id (int), tx_timestamp (datetime),
#   total_amount (float)
#
# transaction_lines:
#   transaction_id (str), line_no (int), product_id (int),
#   brand_id (int), quantity (int), price_unit (float), subtotal (float)
#
# shelf_vision_events:
#   id (str), store_id (int), event_timestamp (datetime),
#   brand_id (int), facings (int), share_of_shelf (float),
#   oos_flag (bool), confidence (float)
#
# stt_events:
#   id (str), store_id (int), event_timestamp (datetime),
#   brand_id (int), raw_text (str), intent_label (str),
#   sentiment_score (float)
#
# weather_daily:
#   id (str), store_id (int), date (date),
#   temp_c (float), rainfall_mm (float), condition (str)
#
# foot_traffic_daily:
#   id (str), store_id (int), date (date),
#   traffic_index (float)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 1. Load raw Kaggle data (CUSTOMIZE HERE)
# ---------------------------------------------------------------------------

def load_raw_kaggle_data():
    """
    Load raw Kaggle-style datasets.

    Assumptions (you can change these to match your actual CSVs):
      - raw_store_sales.csv:
          cols: ['date', 'store_nbr', 'family', 'sales', 'onpromotion']
      - raw_orders.csv:
          cols: ['order_id', 'customer_id', 'order_purchase_timestamp', 'store_nbr']
      - raw_order_products.csv:
          cols: ['order_id', 'product_id', 'add_to_cart_order', 'quantity']
      - raw_products.csv:
          cols: ['product_id', 'product_name', 'category', 'brand_name']
      - raw_stores.csv:
          cols: ['store_nbr', 'city', 'state']  # or similar

    Returns:
        dict of DataFrames keyed by name.
    """
    dfs = {}

    # Check if files exist before reading, to avoid crashing if empty
    # For now, we'll create dummy dataframes if files are missing so the script runs
    # This allows the user to run it immediately to see the structure
    
    def read_or_dummy(filename, dummy_data):
        path = RAW_DIR / filename
        if path.exists():
            return pd.read_csv(path)
        print(f"[WARN] {filename} not found, using dummy data.")
        return pd.DataFrame(dummy_data)

    dfs["store_sales"] = read_or_dummy("raw_store_sales.csv", {
        'date': [datetime.now()], 'store_nbr': [1], 'family': ['Food'], 'sales': [100], 'onpromotion': [0]
    })
    dfs["orders"] = read_or_dummy("raw_orders.csv", {
        'order_id': ['ord1'], 'customer_id': ['cust1'], 'order_purchase_timestamp': [datetime.now()], 'store_nbr': [1]
    })
    dfs["order_products"] = read_or_dummy("raw_order_products.csv", {
        'order_id': ['ord1'], 'product_id': [101], 'add_to_cart_order': [1], 'quantity': [2]
    })
    dfs["products_raw"] = read_or_dummy("raw_products.csv", {
        'product_id': [101], 'product_name': ['Test Product'], 'category': ['Snacks'], 'brand_name': ['Test Brand']
    })
    dfs["stores_raw"] = read_or_dummy("raw_stores.csv", {
        'store_nbr': [1], 'city': ['Manila'], 'state': ['NCR']
    })
    
    # Ensure datetime columns are parsed
    if not dfs["store_sales"].empty and 'date' in dfs["store_sales"].columns:
        dfs["store_sales"]['date'] = pd.to_datetime(dfs["store_sales"]['date'])
    if not dfs["orders"].empty and 'order_purchase_timestamp' in dfs["orders"].columns:
        dfs["orders"]['order_purchase_timestamp'] = pd.to_datetime(dfs["orders"]['order_purchase_timestamp'])

    return dfs


# ---------------------------------------------------------------------------
# 2. Dimensional tables: brands, products, stores
# ---------------------------------------------------------------------------

def build_dim_brands_products(products_raw: pd.DataFrame):
    """
    Build brands and products dims from raw products.

    Expected input cols (customize to match Kaggle):
      - product_id
      - product_name
      - category
      - brand_name

    Returns:
        brands_df, products_df
    """
    # Create brands dim
    brands_df = (
        products_raw
        .rename(columns={"brand_name": "brand_name", "category": "category"})
        [["brand_name", "category"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    brands_df.insert(0, "brand_id", brands_df.index + 1)

    # Merge brand_id back into products
    products_df = products_raw.merge(
        brands_df,
        on=["brand_name", "category"],
        how="left"
    )

    # Add SariCoach specific fields
    products_df["sku"] = products_df["product_id"].astype(str)
    # Fake EAN: 13-digit with product_id suffix
    products_df["barcode"] = products_df["product_id"].apply(
        lambda pid: f"4800{int(pid):09d}"[:13]
    )
    # Simple pack_size / pack_type defaults
    products_df["pack_size"] = "1 unit"
    products_df["pack_type"] = "pack"

    # Reorder columns
    products_df = products_df[[
        "product_id", "sku", "barcode", "brand_id",
        "product_name", "category", "pack_size", "pack_type"
    ]]

    return brands_df, products_df


def build_dim_stores(stores_raw: pd.DataFrame):
    """
    Build stores dim from raw stores.

    Expected input cols (customize):
      - store_nbr
      - city
      - state

    Returns:
        stores_df
    """
    def make_store_name(row):
        return f"Aling Nena Sari-Sari Store #{row['store_id']} – {row['city']}"

    stores_df = stores_raw.copy()
    stores_df = stores_df.rename(columns={"store_nbr": "store_id"})
    stores_df["store_name"] = stores_df.apply(make_store_name, axis=1)

    # Synthetic PH geo (you can refine later)
    stores_df["region"] = "NCR"
    stores_df["barangay"] = "Barangay 1"
    stores_df["store_type"] = "sari-sari"

    stores_df = stores_df[[
        "store_id", "store_name", "region",
        "city", "barangay", "store_type"
    ]]

    return stores_df


# ---------------------------------------------------------------------------
# 3. Fact tables: transactions, transaction_lines
# ---------------------------------------------------------------------------

def build_transactions_and_lines(
    orders: pd.DataFrame,
    order_products: pd.DataFrame,
    products_df: pd.DataFrame,
    stores_df: pd.DataFrame,
    max_days: int = 90,
):
    """
    Build canonical transactions and transaction_lines from Kaggle-like orders.

    Assumes:
      - orders: ['order_id', 'customer_id', 'order_purchase_timestamp', 'store_nbr']
      - order_products: ['order_id', 'product_id', 'quantity' or implicit = 1]

    Returns:
        transactions_df, transaction_lines_df
    """
    # Restrict to last N days for runtime
    max_ts = orders["order_purchase_timestamp"].max()
    cutoff_ts = max_ts - pd.Timedelta(days=max_days)
    orders = orders[orders["order_purchase_timestamp"] >= cutoff_ts].copy()

    # Map to store_id; if store_nbr missing, randomly assign
    if "store_nbr" in orders.columns:
        orders = orders.rename(columns={"store_nbr": "store_id"})
    else:
        store_ids = stores_df["store_id"].tolist()
        orders["store_id"] = orders["order_id"].apply(lambda _: random.choice(store_ids))

    # Build transactions_df
    transactions_df = orders[[
        "order_id", "store_id", "order_purchase_timestamp"
    ]].copy()
    transactions_df = transactions_df.rename(columns={
        "order_id": "transaction_id",
        "order_purchase_timestamp": "tx_timestamp"
    })

    # Merge products into order_products
    op = order_products.merge(products_df[["product_id", "brand_id"]], on="product_id", how="left")

    if "quantity" not in op.columns:
        op["quantity"] = 1

    # Merge in unit price via a simple random scheme if not available
    if "price_unit" not in op.columns:
        # assign category-level price bands
        price_lookup = (
            products_df[["product_id", "category"]]
            .drop_duplicates()
            .assign(price_unit=lambda df: df["category"].map({
                "Beverages": 25,
                "Snacks": 15,
                "Tobacco": 80,
            }).fillna(20))
        )
        op = op.merge(price_lookup[["product_id", "price_unit"]], on="product_id", how="left")

    op["subtotal"] = op["price_unit"] * op["quantity"]

    # Build transaction_lines_df
    op = op.rename(columns={"order_id": "transaction_id"})
    op["line_no"] = op.groupby("transaction_id").cumcount() + 1

    transaction_lines_df = op[[
        "transaction_id", "line_no", "product_id",
        "brand_id", "quantity", "price_unit", "subtotal"
    ]]

    # Aggregate total_amount per transaction
    totals = transaction_lines_df.groupby("transaction_id")["subtotal"].sum().reset_index()
    totals = totals.rename(columns={"subtotal": "total_amount"})
    transactions_df = transactions_df.merge(totals, on="transaction_id", how="left")

    return transactions_df, transaction_lines_df


# ---------------------------------------------------------------------------
# 4. Synthetic multimodal features: shelf vision, STT, weather, traffic
# ---------------------------------------------------------------------------

def generate_shelf_vision(
    transaction_lines_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
    stores_df: pd.DataFrame,
):
    """
    Generate synthetic shelf_vision_events from sales.

    Logic:
      - For each store, brand, day:
          - Compute daily quantity sold.
          - Map to 'facings' via bins.
          - Compute share_of_shelf within category per store/day.
          - Randomly mark occasional OOS where sales drop to zero.

    Returns:
        shelf_vision_df
    """
    tx = transactions_df.copy()
    tx["date"] = tx["tx_timestamp"].dt.date

    tl = transaction_lines_df.merge(
        tx[["transaction_id", "store_id", "date"]],
        on="transaction_id",
        how="left"
    )

    daily_brand = (
        tl.groupby(["store_id", "date", "brand_id"])["quantity"]
        .sum()
        .reset_index()
        .rename(columns={"quantity": "qty_sold"})
    )

    # Map qty_sold -> facings
    def qty_to_facings(q):
        if q >= 20:
            return np.random.randint(8, 12)
        elif q >= 10:
            return np.random.randint(4, 8)
        elif q > 0:
            return np.random.randint(1, 4)
        else:
            return 1

    daily_brand["facings"] = daily_brand["qty_sold"].apply(qty_to_facings)

    # Share of shelf per store/day (within all brands)
    shelf_totals = (
        daily_brand.groupby(["store_id", "date"])["facings"]
        .sum()
        .reset_index()
        .rename(columns={"facings": "facings_total"})
    )
    sv = daily_brand.merge(shelf_totals, on=["store_id", "date"], how="left")
    sv["share_of_shelf"] = sv["facings"] / sv["facings_total"].replace(0, 1)
    sv["oos_flag"] = sv["qty_sold"] == 0

    # Add timestamps, ids, confidence
    sv["event_timestamp"] = sv["date"].apply(
        lambda d: datetime.combine(d, datetime.min.time()) + timedelta(hours=8)
    )
    sv["confidence"] = np.random.uniform(0.8, 0.99, size=len(sv))
    sv["id"] = [str(uuid.uuid4()) for _ in range(len(sv))]

    shelf_vision_df = sv[[
        "id", "store_id", "event_timestamp", "brand_id",
        "facings", "share_of_shelf", "oos_flag", "confidence"
    ]]

    return shelf_vision_df


def generate_stt_events(
    shelf_vision_df: pd.DataFrame,
    max_events_per_day: int = 5,
):
    """
    Generate synthetic STT events per store/brand/day based on facings.

    Heuristic:
      - More facings -> higher chance of mentions.
      - Generate Filipino/Taglish templates as raw_text.
    """
    sv = shelf_vision_df.copy()
    sv["date"] = sv["event_timestamp"].dt.date

    # Aggregate to daily brand shelf presence
    daily = (
        sv.groupby(["store_id", "date", "brand_id"])["facings"]
        .mean()
        .reset_index()
    )

    stt_rows = []
    intents = ["ask_price", "searching", "complaint", "promo_interest"]
    templates = {
        "ask_price": "Magkano po yung {brand}?",
        "searching": "Meron pa bang {brand}?",
        "complaint": "Parang tumaas yung {brand} ah.",
        "promo_interest": "May promo ba sa {brand} ngayon?"
    }

    for _, row in daily.iterrows():
        store_id = row["store_id"]
        brand_id = row["brand_id"]
        date = row["date"]
        facings = row["facings"]

        # Expected mentions ~ facings / scale
        lam = max(0.5, facings / 6.0)
        n_events = np.random.poisson(lam)
        n_events = min(n_events, max_events_per_day)

        for _ in range(n_events):
            intent = random.choice(intents)
            # placeholder, resolved later if you want brand_name
            brand_placeholder = f"Brand {brand_id}"
            raw_text = templates[intent].format(brand=brand_placeholder)

            # Sentiment heuristic
            if intent == "complaint":
                sentiment = np.random.uniform(-0.7, -0.1)
            elif intent == "promo_interest":
                sentiment = np.random.uniform(0.1, 0.6)
            else:
                sentiment = np.random.uniform(-0.2, 0.4)

            ts = datetime.combine(date, datetime.min.time()) + timedelta(
                hours=np.random.randint(8, 20),
                minutes=np.random.randint(0, 60)
            )

            stt_rows.append({
                "id": str(uuid.uuid4()),
                "store_id": store_id,
                "event_timestamp": ts,
                "brand_id": brand_id,
                "raw_text": raw_text,
                "intent_label": intent,
                "sentiment_score": sentiment,
            })

    if not stt_rows:
        # Ensure header exists even if no events generated
        stt_df = pd.DataFrame(columns=[
            "id", "store_id", "event_timestamp", "brand_id",
            "raw_text", "intent_label", "sentiment_score"
        ])
    else:
        stt_df = pd.DataFrame(stt_rows)
    
    return stt_df


def generate_weather_and_traffic(
    stores_df: pd.DataFrame,
    transactions_df: pd.DataFrame,
):
    """
    Generate synthetic daily weather and foot traffic per store
    over the observed transaction date range.
    """
    tx = transactions_df.copy()
    tx["date"] = tx["tx_timestamp"].dt.date

    date_range = pd.date_range(tx["date"].min(), tx["date"].max(), freq="D")
    records_weather = []
    records_traffic = []

    for _, store in stores_df.iterrows():
        store_id = store["store_id"]

        for d in date_range:
            # Weather
            temp_c = np.random.normal(30, 1.5)
            is_rainy = np.random.rand() < 0.3
            rainfall_mm = np.random.exponential(8) if is_rainy else 0.0
            condition = "Rainy" if is_rainy else "Cloudy"

            records_weather.append({
                "id": str(uuid.uuid4()),
                "store_id": store_id,
                "date": d.date(),
                "temp_c": round(temp_c, 1),
                "rainfall_mm": round(rainfall_mm, 1),
                "condition": condition,
            })

            # Foot traffic index
            dow = d.weekday()  # 0=Mon
            base = 100.0
            if dow >= 5:  # weekend
                base *= 1.2
            if is_rainy:
                base *= 0.85

            noise = np.random.normal(0, 10)
            traffic_index = max(20.0, base + noise)

            records_traffic.append({
                "id": str(uuid.uuid4()),
                "store_id": store_id,
                "date": d.date(),
                "traffic_index": round(traffic_index, 1),
            })

    weather_df = pd.DataFrame(records_weather)
    traffic_df = pd.DataFrame(records_traffic)

    return weather_df, traffic_df


# ---------------------------------------------------------------------------
# 5. Export helpers
# ---------------------------------------------------------------------------

def export_csv(name: str, df: pd.DataFrame) -> Path:
    path = OUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"[OK] wrote {path}")
    return path


def export_sql_insert(
    table_name: str,
    df: pd.DataFrame,
    sql_file: Path,
    batch_size: int = 1000,
):
    """
    Very simple Postgres INSERT generator for seeding.

    NOTE: For large data, you'd prefer COPY FROM STDIN; this is enough
    for a small eval dataset.
    """
    cols = list(df.columns)
    col_list = ", ".join(cols)

    with sql_file.open("a", encoding="utf-8") as f:
        for i in range(0, len(df), batch_size):
            chunk = df.iloc[i:i+batch_size]
            values_sql = []
            for _, row in chunk.iterrows():
                vals = []
                for c in cols:
                    v = row[c]
                    if pd.isna(v):
                        vals.append("NULL")
                    elif isinstance(v, (int, float)):
                        vals.append(str(v))
                    elif isinstance(v, (datetime, pd.Timestamp)):
                        vals.append(f"'{v.isoformat()}'")
                    else:
                        # escape single quotes
                        s = str(v).replace("'", "''")
                        vals.append(f"'{s}'")
                values_sql.append(f"({', '.join(vals)})")
            if not values_sql:
                continue
            f.write(f"INSERT INTO {table_name} ({col_list}) VALUES\n")
            f.write(",\n".join(values_sql))
            f.write(";\n\n")


# ---------------------------------------------------------------------------
# 6. Main
# ---------------------------------------------------------------------------

def main():
    print("[*] Loading raw Kaggle-style data...")
    dfs = load_raw_kaggle_data()

    print("[*] Building dims: brands, products, stores...")
    brands_df, products_df = build_dim_brands_products(dfs["products_raw"])
    stores_df = build_dim_stores(dfs["stores_raw"])

    print("[*] Building transactions + transaction_lines...")
    transactions_df, transaction_lines_df = build_transactions_and_lines(
        dfs["orders"],
        dfs["order_products"],
        products_df,
        stores_df,
        max_days=90,
    )

    print("[*] Generating shelf_vision_events...")
    shelf_vision_df = generate_shelf_vision(transaction_lines_df, transactions_df, stores_df)

    print("[*] Generating stt_events...")
    stt_df = generate_stt_events(shelf_vision_df)

    print("[*] Generating weather_daily + foot_traffic_daily...")
    weather_df, traffic_df = generate_weather_and_traffic(stores_df, transactions_df)

    # Export CSVs
    print("[*] Exporting CSVs...")
    export_csv("brands", brands_df)
    export_csv("products", products_df)
    export_csv("stores", stores_df)
    export_csv("transactions", transactions_df)
    export_csv("transaction_lines", transaction_lines_df)
    export_csv("shelf_vision_events", shelf_vision_df)
    export_csv("stt_events", stt_df)
    export_csv("weather_daily", weather_df)
    export_csv("foot_traffic_daily", traffic_df)

    # Optional SQL export
    sql_path = OUT_DIR / "seed_saricoach.sql"
    if sql_path.exists():
        sql_path.unlink()
    print(f"[*] Exporting Postgres INSERTs to {sql_path}...")

    with sql_path.open("w", encoding="utf-8") as f:
        f.write("CREATE SCHEMA IF NOT EXISTS saricoach;\n\n")
        
        # Define tables
        f.write("""
        CREATE TABLE IF NOT EXISTS saricoach.brands (
            brand_id INT PRIMARY KEY,
            brand_name TEXT,
            category TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.products (
            product_id INT PRIMARY KEY,
            sku TEXT,
            barcode TEXT,
            brand_id INT,
            product_name TEXT,
            category TEXT,
            pack_size TEXT,
            pack_type TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.stores (
            product_name TEXT,
            category TEXT,
            pack_size TEXT,
            pack_type TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.stores (
            store_id INT PRIMARY KEY,
            store_name TEXT,
            region TEXT,
            city TEXT,
            barangay TEXT,
            store_type TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.transactions (
            transaction_id TEXT PRIMARY KEY,
            store_id INT,
            tx_timestamp TIMESTAMP,
            total_amount FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.transaction_lines (
            transaction_id TEXT,
            line_no INT,
            product_id INT,
            brand_id INT,
            quantity INT,
            price_unit FLOAT,
            subtotal FLOAT,
            PRIMARY KEY (transaction_id, line_no)
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.shelf_vision_events (
            id TEXT PRIMARY KEY,
            store_id INT,
            event_timestamp TIMESTAMP,
            brand_id INT,
            facings INT,
            share_of_shelf FLOAT,
            oos_flag BOOLEAN,
            confidence FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.stt_events (
            id TEXT PRIMARY KEY,
            store_id INT,
            event_timestamp TIMESTAMP,
            brand_id INT,
            raw_text TEXT,
            intent_label TEXT,
            sentiment_score FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.weather_daily (
            id TEXT PRIMARY KEY,
            store_id INT,
            date DATE,
            temp_c FLOAT,
            rainfall_mm FLOAT,
            condition TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.foot_traffic_daily (
            id TEXT PRIMARY KEY,
            store_id INT,
            date DATE,
            traffic_index FLOAT
        );
        \n""")

    export_sql_insert("saricoach.brands", brands_df, sql_path)
    export_sql_insert("saricoach.products", products_df, sql_path)
    export_sql_insert("saricoach.stores", stores_df, sql_path)
    export_sql_insert("saricoach.transactions", transactions_df, sql_path)
    export_sql_insert("saricoach.transaction_lines", transaction_lines_df, sql_path)
    export_sql_insert("saricoach.shelf_vision_events", shelf_vision_df, sql_path)
    export_sql_insert("saricoach.stt_events", stt_df, sql_path)
    export_sql_insert("saricoach.weather_daily", weather_df, sql_path)
    export_sql_insert("saricoach.foot_traffic_daily", traffic_df, sql_path)

    print("[✓] SariCoach seed data generation complete.")


if __name__ == "__main__":
    main()
