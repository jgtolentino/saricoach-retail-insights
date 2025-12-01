# Deployment Guide – SariCoach

SariCoach supports two environments:

1. **Supabase mode (primary)** – production-style deployment using a real Postgres database.
2. **CSV mode (optional)** – offline / Kaggle demo using local CSVs only.

The Kaggle CSVs are used as **seed inputs**; the live system runs entirely on Supabase.

---

## 1. Supabase Mode (Primary Runtime)

### 1.1. Prerequisites

- Supabase project created.
- Postgres connection string (DATABASE_URL).
- Python 3.11+
- Node.js (for the dashboard).

### 1.2. Apply Schema and Seed

From the project root:

```bash
# 1) Apply core schema
export DATABASE_URL="postgres://<user>:<pass>@<host>:<port>/<db_name>"

psql "$DATABASE_URL" -f supabase/schema/001_saricoach_schema.sql

# 2) Apply demo / synthetic seed data
psql "$DATABASE_URL" -f supabase/seed/seed_saricoach.sql
```

This creates and populates the `saricoach.*` tables.

---

## 2. Run the API Against Supabase

The FastAPI service always reads from the database in this mode.

```bash
# Environment
export SARICOACH_DATA_BACKEND=supabase
export DATABASE_URL="postgres://<user>:<pass>@<host>:<port>/<db_name>"

# Optional: enable Gemini-powered coaching if you have a key
# export SARICOACH_GOOGLE_API_KEY="your_gemini_key"

# Install deps
pip install -r requirements.txt

# Run API
uvicorn service.app.main:app --host 0.0.0.0 --port 8000
```

Key endpoints:

* `GET /api/health` – health check
* `GET /api/store/{store_id}/summary` – KPIs + coach output for a store
* `POST /api/coach/recommendations` – structured coaching request/response

See `docs/API.md` for payload details.

---

## 3. Deploy the React Mobile Dashboard

From `dashboard/`:

```bash
cd dashboard
npm install

# Local dev
VITE_API_URL=http://localhost:8000 npm run dev
```

For Netlify / Vercel:

* Set `VITE_API_URL` in project environment variables to your deployed API URL (e.g. `https://api.saricoach.example.com`).
* Build and deploy with their standard React/Vite flow (`npm run build`).

The dashboard does **not** talk to CSVs; it only talks to the FastAPI API.

---

## 4. CSV / Kaggle Mode (Optional Demo)

For the Kaggle notebook and pure-offline demos, you can still use the processed CSVs:

1. Generate processed data from raw Kaggle-style inputs:

   ```bash
   python3 seed_saricoach_data.py
   ```

   This writes:

   * `data/processed/*.csv` – canonical tables
   * `data/processed/seed_saricoach.sql` – seed file used above

2. In the **notebook**, the SariCoach code reads `data/processed/*.csv` directly (no DB, no network).

This keeps the Kaggle submission self-contained while the deployed app uses Supabase as its single source of truth.
