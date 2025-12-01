from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any

class Kpi(BaseModel):
    label: str
    value: Union[float, int, str]
    delta_pct: Optional[float] = None
    trend: str = "neutral"  # up, down, neutral

class StoreSummary(BaseModel):
    store_id: int
    store_name: str
    period: str
    kpis: List[Kpi]
    chart: List[Dict[str, Any]]   # [{date, volume}, ...]
    insights: List[str]
    coach_message: str
