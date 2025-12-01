import os
from pathlib import Path
from saricoach.data_context import DataContext
from saricoach.backends.csv_backend import build_context_from_csv
from saricoach.backends.supabase_backend import build_context_from_supabase
from saricoach.agents.planner import PlannerAgent
from saricoach.agents.data_analyst import DataAnalystAgent
from saricoach.agents.coach import CoachAgent

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"

from typing import Optional

_backend = os.getenv("SARICOACH_DATA_BACKEND", "csv")

_ctx: Optional[DataContext] = None
_planner: Optional[PlannerAgent] = None
_analyst: Optional[DataAnalystAgent] = None
_coach: Optional[CoachAgent] = None

def get_context() -> DataContext:
    global _ctx
    if _ctx is None:
        if _backend == "supabase":
            _ctx = build_context_from_supabase()
        else:
            _ctx = build_context_from_csv(DATA_DIR)
    return _ctx

def get_agents() -> tuple[PlannerAgent, DataAnalystAgent, CoachAgent]:
    global _planner, _analyst, _coach
    ctx = get_context()
    if _planner is None:
        _planner = PlannerAgent()
    if _analyst is None:
        _analyst = DataAnalystAgent(ctx=ctx)
    if _coach is None:
        api_key = os.getenv("SARICOACH_GOOGLE_API_KEY")
        use_gemini = bool(api_key)
        _coach = CoachAgent(model_name="gemini" if use_gemini else "heuristic",
                            use_gemini=use_gemini)
    return _planner, _analyst, _coach
