import os
import psycopg
from dotenv import load_dotenv

load_dotenv(".env.local")

def apply_schema_and_seed():
    db_url = os.getenv("POSTGRES_URL_NON_POOLING") or os.getenv("POSTGRES_URL")
    if not db_url:
        print("❌ Error: DATABASE_URL is missing.")
        return

    schema_path = "supabase/schema/001_saricoach_schema.sql"
    seed_path = "supabase/seed/seed_saricoach.sql"

    try:
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                print("✅ Connected to Supabase...")
                
                # Apply Schema
                if os.path.exists(schema_path):
                    print(f"Applying schema from {schema_path}...")
                    with open(schema_path, "r") as f:
                        cur.execute(f.read())
                    print("✅ Schema applied.")
                else:
                    print(f"❌ Schema file not found: {schema_path}")

                # Apply Seed
                if os.path.exists(seed_path):
                    print(f"Applying seed from {seed_path}...")
                    with open(seed_path, "r") as f:
                        cur.execute(f.read())
                    print("✅ Seed data applied.")
                else:
                    print(f"❌ Seed file not found: {seed_path}")
                
                conn.commit()
                print("✅ Database setup complete.")

    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    apply_schema_and_seed()
