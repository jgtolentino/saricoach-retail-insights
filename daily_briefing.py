# Cell 1: Setup & Imports
import os
import psycopg
import google.generativeai as genai
from dotenv import load_dotenv

# Load from .env.local for Vercel/Supabase credentials
load_dotenv(".env.local")
genai.configure(api_key=os.getenv("SARICOACH_GOOGLE_API_KEY"))

# Use POSTGRES_URL if available, else DATABASE_URL
DB_URL = os.getenv("POSTGRES_URL_NON_POOLING") or os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")

# Cell 2: The Analyst Agent (Fetches & Processes Data)
def get_daily_context(store_id=1):
    if not DB_URL:
        print("❌ Error: DATABASE_URL is missing.")
        return None

    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            # Get Metrics for Manila Time
            cur.execute("""
                SELECT volume, revenue, avg_basket_size 
                FROM daily_metrics WHERE store_id=%s AND date=(now() at time zone 'Asia/Manila')::date
            """, (store_id,))
            metrics = cur.fetchone()
            
            if not metrics:
                print("⚠️ No metrics found for today.")
                return None

            # Get Traffic Patterns
            cur.execute("""
                SELECT hour_of_day, volume FROM hourly_traffic 
                WHERE store_id=%s AND date=(now() at time zone 'Asia/Manila')::date
                ORDER BY volume DESC LIMIT 1
            """, (store_id,))
            peak = cur.fetchone()
            
            return {
                "revenue": metrics[1],
                "volume": metrics[0],
                "basket": metrics[2],
                "peak_hour": f"{peak[0]}:00" if peak else "N/A",
                "peak_vol": peak[1] if peak else 0
            }

# Cell 3: The Coach Agent (Generates Strategy)
def generate_daily_briefing(context):
    if not context:
        return "No data available for analysis today."

    # Using gemini-2.0-flash as verified
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Analyze this daily retail snapshot and write a 1-sentence 'Coach Message' 
    for the store owner. Focus on the most notable stat.
    
    Data:
    - Revenue: {context['revenue']}
    - Volume: {context['volume']} transactions
    - Peak Hour: {context['peak_hour']} (Volume: {context['peak_vol']})
    
    Output Format: Just the message string. No markdown.
    """
    
    response = model.generate_content(prompt)
    return response.text.strip()

# Cell 4: The Writer (Updates DB)
def update_store_insight(store_id, message):
    if not DB_URL:
        return

    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE daily_insights 
                SET coach_message = %s 
                WHERE store_id = %s AND date = (now() at time zone 'Asia/Manila')::date
            """, (message, store_id))
            conn.commit()
    print(f"✅ Database updated with insight: {message}")

# Cell 5: EXECUTE PIPELINE
if __name__ == "__main__":
    print("🤖 Agent waking up...")
    data = get_daily_context(1)
    if data:
        print(f"📊 Analyzed data: {data}")
        insight = generate_daily_briefing(data)
        print(f"💡 Generated Insight: {insight}")
        update_store_insight(1, insight)
    else:
        print("❌ Failed to get data context.")
