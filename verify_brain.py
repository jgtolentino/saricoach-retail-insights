
import sys
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.append(".")

try:
    from src.feature_frame import DataContext
    from src.agents.core import PlannerAgent, DataAnalystAgent, CoachAgent
    print("✅ Imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

BASE = Path("data/processed")

if not BASE.exists():
    print("⚠️ data/processed not found, skipping data loading check")
    sys.exit(0)

try:
    brands = pd.read_csv(BASE / "brands.csv")
    products = pd.read_csv(BASE / "products.csv")
    stores = pd.read_csv(BASE / "stores.csv")
    transactions = pd.read_csv(BASE / "transactions.csv", parse_dates=["tx_timestamp"])
    transaction_lines = pd.read_csv(BASE / "transaction_lines.csv")
    shelf_vision = pd.read_csv(BASE / "shelf_vision_events.csv", parse_dates=["event_timestamp"])
    stt_events = pd.read_csv(BASE / "stt_events.csv", parse_dates=["event_timestamp"])
    weather = pd.read_csv(BASE / "weather_daily.csv", parse_dates=["date"])
    foot_traffic = pd.read_csv(BASE / "foot_traffic_daily.csv", parse_dates=["date"])

    ctx = DataContext(
        brands=brands,
        products=products,
        stores=stores,
        transactions=transactions,
        transaction_lines=transaction_lines,
        shelf_vision=shelf_vision,
        stt_events=stt_events,
        weather=weather,
        foot_traffic=foot_traffic,
    )
    print("✅ DataContext initialized")

    planner = PlannerAgent()
    analyst = DataAnalystAgent(ctx=ctx)
    coach = CoachAgent(model_name="heuristic", use_gemini=False)
    print("✅ Agents initialized")

    # Test run
    sample_store_id = int(stores.iloc[0]["store_id"])
    decision = planner.plan({
        "type": "seven_day_plan",
        "store_id": sample_store_id,
        "days": 30,
    })
    analytics = analyst.analyze(decision)
    coach_output = coach.coach(analytics)
    
    print(f"✅ Agent loop successful. Generated {len(coach_output.actions)} actions.")

except Exception as e:
    print(f"❌ Verification failed: {e}")
    sys.exit(1)
