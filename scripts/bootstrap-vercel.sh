#!/usr/bin/env bash
set -euo pipefail

# === CONFIG – EDIT THESE 5 VALUES ONLY ===
VERCEL_PROJECT_NAME="saricoach-retail-insights"

# REPLACE THESE WITH YOUR ACTUAL SUPABASE CREDENTIALS
SUPABASE_URL="https://YOUR-PROJECT.supabase.co"
SUPABASE_ANON_KEY="YOUR_ANON_KEY"
SUPABASE_SERVICE_ROLE_KEY="YOUR_SERVICE_ROLE_KEY"

SARICOACH_GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
# =========================================

# 0) Go to repo
# cd ~/code/saricoach-retail-insights # Commented out as user might run from root

# 1) Ensure Vercel project is linked
vercel link --project "$VERCEL_PROJECT_NAME" --yes || true

# Function to add env var safely
add_env() {
    local key="$1"
    local val="$2"
    local envs=("production" "preview" "development")
    
    for env in "${envs[@]}"; do
        # Try to remove first to avoid duplicates/errors if it exists
        vercel env rm "$key" "$env" --yes || true
        printf "%s" "$val" | vercel env add "$key" "$env"
    done
}

# 2) FRONTEND VARS (Vite + Supabase + API base)
add_env VITE_SUPABASE_URL "$SUPABASE_URL"
add_env VITE_SUPABASE_ANON_KEY "$SUPABASE_ANON_KEY"

# API base = this Vercel app itself (can change to custom domain later)
APP_URL="https://${VERCEL_PROJECT_NAME}.vercel.app"
add_env VITE_API_URL "$APP_URL"

# 3) BACKEND VARS (FastAPI + Supabase)
add_env SUPABASE_URL "$SUPABASE_URL"
add_env SUPABASE_ANON_KEY "$SUPABASE_ANON_KEY"
add_env SUPABASE_SERVICE_ROLE_KEY "$SUPABASE_SERVICE_ROLE_KEY"

# 4) GEMINI KEY FOR AGENT LAYER
add_env SARICOACH_GOOGLE_API_KEY "$SARICOACH_GOOGLE_API_KEY"

# 5) Pull env vars locally for dev (creates .env.local)
vercel env pull .env.local

# 6) Install deps and run type-safe build check locally
npm install
npm run build

# 7) Deploy to Vercel (production)
vercel --prod --confirm
