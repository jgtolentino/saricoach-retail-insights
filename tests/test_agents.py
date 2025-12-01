from pathlib import Path
import pandas as pd
import pytest

from saricoach.agents.planner import PlannerAgent
from saricoach.agents.data_analyst import DataAnalystAgent
from saricoach.agents.coach import CoachAgent
from saricoach.data_context import DataContext

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"

def _load_ctx() -> DataContext:
    # Ensure data exists (test_seed_script should run first or data should be present)
    if not (DATA_DIR / "brands.csv").exists():
        pytest.skip("Processed data not found. Run seed script first.")

    return DataContext(
        brands=pd.read_csv(DATA_DIR / "brands.csv"),
        products=pd.read_csv(DATA_DIR / "products.csv"),
        stores=pd.read_csv(DATA_DIR / "stores.csv"),
        transactions=pd.read_csv(DATA_DIR / "transactions.csv", parse_dates=["tx_timestamp"]),
        transaction_lines=pd.read_csv(DATA_DIR / "transaction_lines.csv"),
        shelf_vision=pd.read_csv(DATA_DIR / "shelf_vision_events.csv", parse_dates=["event_timestamp"]),
        stt_events=pd.read_csv(DATA_DIR / "stt_events.csv", parse_dates=["event_timestamp"]),
        weather=pd.read_csv(DATA_DIR / "weather_daily.csv", parse_dates=["date"]),
        foot_traffic=pd.read_csv(DATA_DIR / "foot_traffic_daily.csv", parse_dates=["date"]),
    )

def test_agent_pipeline_runs_for_demo_store():
    ctx = _load_ctx()
    planner = PlannerAgent()
    analyst = DataAnalystAgent(ctx=ctx)
    coach = CoachAgent(model_name="heuristic", use_gemini=False)

    decision = planner.plan({"type": "seven_day_plan", "store_id": 1, "days": 30})
    analytics = analyst.analyze(decision)
    output = coach.coach(analytics, persona="store_owner")

    assert output.actions, "Coach should return at least one action"
    assert isinstance(output.actions[0], str)
    assert isinstance(output.debug_notes, dict)
