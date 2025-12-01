# Hybrid Deployment Guide – SariCoach 🚀

SariCoach uses a **Hybrid Cloud Architecture** to combine the best of Serverless (Frontend) and Dedicated Compute (Backend).

## 🏗️ Why Hybrid?

| Component | Technology | Why? |
| :--- | :--- | :--- |
| **Frontend** | **Vercel (Edge)** | Instant global loading, zero-config CI/CD, and free SSL. |
| **Backend** | **DigitalOcean Droplet** | **Heavy Compute:** The AI Agent processes large Pandas DataFrames and maintains state, which hits Vercel's 250MB / 10s timeout limits. A dedicated 8GB RAM Droplet ensures stability. |
| **Database** | **Supabase** | Managed PostgreSQL with Connection Pooling (pgbouncer) to handle high concurrency from the backend. |

---

## 🌊 Backend Deployment (DigitalOcean)

The backend is hosted on a standard Ubuntu Droplet.

### 1. Access the Server
```bash
ssh root@188.166.237.231
```

### 2. Initial Setup (One-Time)
```bash
# Update system
apt update && apt upgrade -y
apt install python3-pip python3-venv git -y

# Clone Repository
git clone https://github.com/jgtolentino/saricoach-retail-insights.git
cd saricoach-retail-insights

# Setup Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r service/requirements.txt
```

### 3. Configure Secrets
Create the `.env` file in `service/.env`:

```bash
nano service/.env
```

**Required Variables:**
```ini
# Database
SARICOACH_DATA_BACKEND=supabase
SARICOACH_DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:6543/postgres?pgbouncer=true

# AI
SARICOACH_GOOGLE_API_KEY=AIza...

# CORS (Allow Vercel)
SARICOACH_CORS_ORIGINS=https://agents-intensive-saricoach.vercel.app,http://localhost:5173
```

### 4. Run the Service
We use `uvicorn` to run the FastAPI app. Use `nohup` to keep it running after disconnect.

```bash
# Stop existing process
pkill uvicorn

# Start new process
nohup uvicorn service.app.main:app --host 0.0.0.0 --port 8000 &

# Verify it's running
tail -f nohup.out
```

---

## ⚡ Frontend Deployment (Vercel)

The frontend is deployed via Vercel Git Integration.

### 1. Vercel Configuration (`vercel.json`)
We use a **Proxy Rewrite** to tunnel API requests to the Droplet. This solves the "Mixed Content" error (HTTPS Frontend -> HTTP Backend).

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "http://188.166.237.231:8000/api/:path*"
    }
  ]
}
```

### 2. Environment Variables
Set these in the Vercel Project Settings:

*   `VITE_API_URL`: `http://188.166.237.231:8000` (Used by the Proxy)
*   `VITE_SUPABASE_URL`: `[Your Supabase URL]`
*   `VITE_SUPABASE_ANON_KEY`: `[Your Supabase Key]`

### 3. Deploy
Push to `main` to trigger a deployment.

---

## 🔄 Updates & Maintenance

To update the backend code:

```bash
ssh root@188.166.237.231
cd saricoach-retail-insights
git pull origin main
pkill uvicorn
nohup uvicorn service.app.main:app --host 0.0.0.0 --port 8000 &
```
