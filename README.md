# SariCoach – Retail Intelligence for Sari-Sari Stores 🏪

![Sanity Check](../../actions/workflows/sanity-check.yml/badge.svg)

SariCoach is a multimodal retail coach for micro-retailers in the Philippines. It combines **Odoo ERP data** with **AI Agents** to provide actionable daily insights.

## 🏗️ Architecture

```ascii
[ React Frontend ] <--> [ FastAPI Backend ] <--> [ Supabase (Postgres) ]
      (Mobile)              (Service)                  (Data)
                               ^
                               |
                        [ Gemini AI ]
                          (Brain)
```

## ✅ Quick Verification

Follow these 3 steps to confirm the system is live:

1.  **Frontend Boot:**
    ```bash
    cd dashboard && npm run dev
    # Visit http://localhost:5173
    ```
2.  **API Health Check:**
    ```bash
    curl http://localhost:8000/api/health
    # Should return: {"status": "ok"}
    ```
3.  **Data Flow Test:**
    ```bash
    curl http://localhost:8000/api/store/1/summary
    # Should return JSON with "store_name", "kpis", etc.
    ```

## 🩺 The Health Check Script

For a full system diagnosis (Backend + DB + AI), run the automated sanity script:

```bash
python check_prod.py
```

**Success Output:**
```text
🚀 Testing Production at http://localhost:8000...
✅ Health Check: OK
✅ Data Fetch: OK (Store: Sari-Sari Store #1)
✨ System Ready for Demo.
```

If this script fails, consult the [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

## 🚀 Getting Started

### 1. Backend Service
```bash
# Install dependencies
pip install -r service/requirements.txt

# Run server
uvicorn service.app.main:app --reload --port 8000
```

### 2. Mobile Dashboard
```bash
cd dashboard
npm install
npm run dev
```

### 3. Environment Variables
Ensure you have a `.env` (or `.env.local`) file in `service/` with:
- `SARICOACH_DATABASE_URL` (Supabase connection)
- `SARICOACH_GOOGLE_API_KEY` (Gemini API)

## 📚 Documentation
- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting & Diagnostics](docs/TROUBLESHOOTING.md)
