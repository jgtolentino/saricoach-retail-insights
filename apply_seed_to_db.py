import os
import psycopg2
from pathlib import Path

# Credentials from user provided context
DB_URL = "postgres://postgres.spdtwktxdalcfigzeqrz:SHWYXDMFAwXI1drT@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"

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
        
        print("✅ Migration successful! Data seeded to 'kaggle' schema.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    main()
