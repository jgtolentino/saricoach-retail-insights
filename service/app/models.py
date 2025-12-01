# service/app/models.py

from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel


Persona = Literal["store_owner", "brand_manager", "distributor"]


class CoachRequest(BaseModel):
    store_id: int
    type: str = "seven_day_plan"
    brand_id: Optional[int] = None
    category: Optional[str] = None
    days: int = 30
    persona: Persona = "store_owner"


class CoachResponse(BaseModel):
    actions: List[str]
    risks: List[str]
    opportunities: List[str]
    debug_notes: Dict[str, Any]


class StoreSummaryResponse(BaseModel):
    store_id: int
    date: str
    kpis: Dict[str, Any]
    coach: CoachResponse
