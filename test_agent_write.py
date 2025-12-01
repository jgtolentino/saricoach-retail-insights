import os
import psycopg
from dotenv import load_dotenv

# Load from .env.local since that's where Vercel pulls valid credentials
load_dotenv(".env.local") 

def test_agent_write():
    # Try DATABASE_URL first, then fallback to constructing it like the backend does
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        # Try POSTGRES_URL directly first (more reliable on Vercel)
        db_url = os.getenv("POSTGRES_URL_NON_POOLING") or os.getenv("POSTGRES_URL")
        
    if not db_url:
        # Fallback logic similar to backend
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        db = os.getenv("POSTGRES_DATABASE")
        
        if user and password and host and db:
            db_url = f"postgresql://{user}:{password}@{host}:5432/{db}"
        else:
            # Try POSTGRES_URL directly
            db_url = os.getenv("POSTGRES_URL_NON_POOLING") or os.getenv("POSTGRES_URL")

    if not db_url:
        print("❌ Error: DATABASE_URL is missing and could not be constructed.")
        return

    print(f"DEBUG: Connecting to {db_url.split('@')[-1] if '@' in db_url else 'UNKNOWN'}")

    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                print("✅ Connected to Supabase...")
                
                # simulate the Agent writing a new insight
                new_insight = "TEST AGENT INSIGHT: Customer foot traffic is high today!"
                
                cur.execute("""
                    UPDATE daily_insights 
                    SET coach_message = %s 
                    WHERE store_id = 1 AND date = CURRENT_DATE
                """, (new_insight,))
                
                print("✅ Agent successfully wrote to DB.")
    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    test_agent_write()
