# Deploying SariCoach to DigitalOcean Droplet 💧

Since Vercel Serverless functions have limitations (IPv4 only, memory limits for Pandas), we are deploying the backend to a dedicated Droplet.

**Target Server:** `188.166.237.231` (8GB RAM)

## 1. Connect to Server
```bash
ssh root@188.166.237.231
```

## 2. Setup Environment
```bash
# Update and install tools
apt update
apt install python3-pip python3-venv git -y

# Clone repo
git clone https://github.com/jgtolentino/saricoach-retail-insights.git
cd saricoach-retail-insights

# Setup Virtual Env
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r service/requirements.txt
```

## 3. Configure Secrets
Create `.env` file:
```bash
nano service/.env
```

**Content:**
```ini
SARICOACH_DATA_BACKEND=supabase
# Use the Pooler URL (Port 6543)
SARICOACH_DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@db.spdtwktxdalcfigzeqrz.supabase.co:6543/postgres?pgbouncer=true
SARICOACH_GOOGLE_API_KEY=[YOUR_GEMINI_KEY]
```

## 4. Run Backend
Run in background using `nohup`:
```bash
nohup uvicorn service.app.main:app --host 0.0.0.0 --port 8000 &
```

## 5. Verify
Check health endpoint:
`http://188.166.237.231:8000/api/health`

## 6. Update Frontend
In Vercel Settings -> Environment Variables:
*   Set `VITE_API_URL` to `http://188.166.237.231:8000`
*   Redeploy Frontend.
