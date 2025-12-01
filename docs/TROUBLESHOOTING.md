# Diagnostics & Troubleshooting Guide 🛠️

This guide helps you identify and fix common issues when running SariCoach.

## 🔍 Common Failure Modes

| Symptom | Likely Cause | Fix |
| :--- | :--- | :--- |
| **Frontend shows "Failed to load store summary"** | Backend not reachable or CORS issue | 1. Ensure backend is running (`uvicorn service.app.main:app`).<br>2. Check browser console for CORS errors.<br>3. Verify `VITE_API_URL` in frontend `.env`. |
| **Coach returns 500 Error** | Gemini API Key missing or invalid | 1. Check `SARICOACH_GOOGLE_API_KEY` in `service/.env` or `.env.local`.<br>2. Ensure the key has quota available. |
| **Database returns empty data** | Connection string or Data missing | 1. Check `SARICOACH_DATABASE_URL` format.<br>2. Ensure you are using the **Transaction Mode** (port 6543) or **Session Mode** (port 5432) correctly.<br>3. Run `python apply_seed_to_db.py` to repopulate data. |
| **Vercel Backend Timeout / 500** | IPv6/IPv4 Mismatch (Vercel is IPv4 only) | **CRITICAL:** Use Supabase **Session Pooler** (Port 6543).<br>URL format: `postgresql://user:pass@host:6543/postgres?pgbouncer=true`.<br>Direct connection (5432) will fail on Vercel. |
| **Agent script runs but no insight appears on UI** | Store ID mismatch or Timezone issue | 1. Ensure script writes to `store_id=1`.<br>2. Check if `date` in DB matches "Today" in Manila time (`Asia/Manila`).<br>3. Verify frontend is fetching for the same `store_id`. |
| **"Network Error" when asking Coach** | Internet connectivity or API Timeout | 1. Check internet connection.<br>2. Verify backend logs for timeout errors.<br>3. Ensure Gemini API is reachable from your network. |

## 🩺 The Health Check Script

We provide a dedicated script to validate the entire pipeline (Backend -> DB -> AI).

### How to Run
```bash
python check_prod.py
```

### Output Reference

**✅ Success Output:**
```text
🚀 Testing Production at http://localhost:8000...
✅ Health Check: OK
✅ Data Fetch: OK (Store: Sari-Sari Store #1)
✨ System Ready for Demo.
```

**❌ Failure Output (Example):**
```text
🚀 Testing Production at http://localhost:8000...
❌ Health Check Failed: 404
```
OR
```text
❌ Data Fetch Failed: 500
```

## 🐛 Debugging Tips

1.  **Backend Logs:** Always keep the terminal running `uvicorn` visible. It shows detailed Python tracebacks.
2.  **Browser Network Tab:** Use Chrome DevTools -> Network to see the raw JSON response from the API.
3.  **Supabase Dashboard:** Use the Table Editor in Supabase to verify if data actually exists in `daily_metrics` and `daily_insights`.
