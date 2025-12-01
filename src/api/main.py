from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import Settings
from src.agents import PlannerAgent


settings = Settings()
planner = PlannerAgent(settings=settings)

app = FastAPI(title="SariCoach Agent Service", version="1.0.0")


class AnalyzeRequest(BaseModel):
    payload: Dict[str, Any]


class AnalyzeResponse(BaseModel):
    summary: str
    recommendations: Dict[str, Any]
    analysis: Dict[str, Any]


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze/store", response_model=AnalyzeResponse)
def analyze_store(req: AnalyzeRequest) -> AnalyzeResponse:
    try:
        result = planner.run(req.payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Internal error") from e

    return AnalyzeResponse(**result)
