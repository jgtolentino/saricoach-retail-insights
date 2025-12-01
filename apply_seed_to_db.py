import os
import psycopg2
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Credentials from environment
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    # Fallback or error
    print("Warning: DATABASE_URL not found in .env. Please set it.")
    # Keep the old one as a fallback comment or just fail? 
    # Better to fail or use a placeholder that won't work but shows intent.
    DB_URL = "postgresql://postgres:[YOUR_PASSWORD]@db.spdtwktxdalcfigzeqrz.supabase.co:5432/postgres"

SQL_FILE = Path("data/processed/seed_saricoach.sql")

def main():
    if not SQL_FILE.exists():
        print(f"Error: {SQL_FILE} not found. Run seed_saricoach_data.py first.")
        return

    print(f"Connecting to Supabase...")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print(f"Reading SQL from {SQL_FILE}...")
        sql_content = SQL_FILE.read_text(encoding="utf-8")
        
        # Split by statement if needed, or execute as one block if simple
        # The seed file uses explicit semicolons.
        
        print("Executing SQL migration...")
        cur.execute(sql_content)
        conn.commit()
        
        print("✅ Migration successful! Data seeded to 'saricoach' schema.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    main()
