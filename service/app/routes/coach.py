from fastapi import APIRouter, Depends
from ..dependencies import get_agents
from ..models import CoachRequest, CoachResponse

router = APIRouter(tags=["coach"])

@router.post("/api/coach/recommendations", response_model=CoachResponse)
def coach_recommendations(req: CoachRequest):
    planner, analyst, coach = get_agents()

    decision = planner.plan({
        "type": req.type,
        "store_id": req.store_id,
        "brand_id": req.brand_id,
        "category": req.category,
        "days": req.days,
    })
    analytics = analyst.analyze(decision)
    coach_output = coach.coach(analytics, persona=req.persona)

    return CoachResponse(
        actions=coach_output.actions,
        risks=coach_output.risks,
        opportunities=coach_output.opportunities,
        debug_notes=coach_output.debug_notes,
    )
