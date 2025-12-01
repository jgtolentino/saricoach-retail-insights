from fastapi import APIRouter, Depends
from datetime import date

from saricoach.analytics import compute_store_kpis
from saricoach.eval.types import AnalyticsResult, CoachOutput
from ..dependencies import get_agents
from ..models import StoreSummaryResponse, CoachResponse

router = APIRouter(tags=["store"])

@router.get("/api/store/{store_id}/summary", response_model=StoreSummaryResponse)
def store_summary(store_id: int):
    planner, analyst, coach = get_agents()

    decision = planner.plan({
        "type": "seven_day_plan",
        "store_id": store_id,
        "days": 30,
    })
    analytics: AnalyticsResult = analyst.analyze(decision)
    coach_output: CoachOutput = coach.coach(analytics, persona="store_owner")

    kpis = compute_store_kpis(analytics, store_id)

    return StoreSummaryResponse(
        store_id=store_id,
        date=str(date.today()),
        kpis=kpis,
        coach=CoachResponse(
            actions=coach_output.actions,
            risks=coach_output.risks,
            opportunities=coach_output.opportunities,
            debug_notes=coach_output.debug_notes,
        ),
    )
