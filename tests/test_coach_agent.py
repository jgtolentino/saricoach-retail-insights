import pytest
import pandas as pd
from saricoach.agents.coach import CoachAgent
from saricoach.eval.types import AnalyticsResult, PlannerDecision

def test_coach_agent_heuristic():
    # Mock AnalyticsResult
    summary = pd.DataFrame({
        "brand_name": ["BrandA"],
        "category": ["Cat1"],
        "risk_stockout_score": [1.0],
        "risk_visibility_score": [0.0],
        "opp_high_demand_score": [0.0],
    })
    
    analytics = AnalyticsResult(
        store_id=1,
        decision=PlannerDecision("seven_day_plan", 1),
        feature_frame=pd.DataFrame(),
        brand_summary=summary
    )
    
    agent = CoachAgent(model_name="heuristic")
    output = agent.coach(analytics)
    
    assert len(output.actions) > 0
    assert len(output.risks) > 0
    assert "stockout" in output.risks[0]
