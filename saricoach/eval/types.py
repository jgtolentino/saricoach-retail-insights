from dataclasses import dataclass
from typing import Literal, Optional, List, Dict, Any
import pandas as pd

FlowType = Literal[
    "analyze_store",
    "explain_brand",
    "seven_day_plan",
]

@dataclass
class PlannerDecision:
    flow: FlowType
    store_id: int
    brand_id: Optional[int] = None
    category: Optional[str] = None
    focus_days: int = 30

@dataclass
class AnalyticsResult:
    store_id: int
    decision: PlannerDecision
    feature_frame: pd.DataFrame
    brand_summary: pd.DataFrame

@dataclass
class CoachOutput:
    actions: List[str]
    risks: List[str]
    opportunities: List[str]
    debug_notes: Dict[str, Any]
