# Supabase Backend – SariCoach

This folder contains the **database schema** and **seed data** used to run SariCoach on Supabase.

SariCoach runs **only on Supabase at runtime**. The CSVs and SQL seed are used once to initialize the database.

---

## 1. Files

- `schema/001_saricoach_schema.sql`
  - Creates the `saricoach` schema and core tables:
    - `saricoach.brands`
    - `saricoach.products`
    - `saricoach.stores`
    - `saricoach.transactions`
    - `saricoach.transaction_lines`
    - `saricoach.shelf_vision_events`
    - `saricoach.stt_events`
    - `saricoach.weather_daily`
    - `saricoach.foot_traffic_daily`
  - Includes foreign keys and indexes optimized for SariCoach queries.

- `seed/seed_saricoach.sql`
  - Inserts demo / synthetic data generated from the Kaggle-style CSVs.
  - This is created by running `seed_saricoach_data.py` from the project root.

---

## 2. Seeding Supabase

1. Create a Supabase project and get the **connection string** (Postgres URI).

2. Apply schema:

   ```bash
   export DATABASE_URL="postgres://<user>:<pass>@<host>:<port>/<db_name>"

   psql "$DATABASE_URL" -f supabase/schema/001_saricoach_schema.sql
   ```

3. Apply seed data:

   ```bash
   psql "$DATABASE_URL" -f supabase/seed/seed_saricoach.sql
   ```

After this, the `saricoach.*` tables are populated and can be used by the FastAPI service and the React dashboard.

---

## 3. Runtime Expectations

In **deployed mode**:

* The API and agents **never read CSV files directly**.
* All data is read from the Supabase Postgres database via `DATABASE_URL`.
* The same schema is also mirrored in `data/processed/*.csv` for offline / Kaggle demos.
