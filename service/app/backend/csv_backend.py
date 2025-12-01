import pandas as pd
from typing import Optional
from .base import DataBackend
from ..models import StoreSummary, Kpi

class CSVBackend(DataBackend):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def fetch_store_summary(self, store_id: int) -> Optional[StoreSummary]:
        # SIMULATION MODE: 
        # In a real scenario, you would read: df = pd.read_csv(f"{self.base_path}/sales.csv")
        # For this skeleton to work immediately, we return a mock structure.
        
        return StoreSummary(
            store_id=store_id,
            store_name=f"Sari-Sari Store #{store_id}",
            period="Today",
            kpis=[
                Kpi(label="Daily Volume", value=649, delta_pct=12.3, trend="up"),
                Kpi(label="Daily Revenue", value="₱135,785", delta_pct=-13.1, trend="down"),
                Kpi(label="Avg Basket", value=2.4, delta_pct=5.7, trend="up"),
                Kpi(label="Avg Duration", value="42s", delta_pct=-8.2, trend="down"),
            ],
            chart=[
                {"date": "08:00", "volume": 45},
                {"date": "10:00", "volume": 120},
                {"date": "12:00", "volume": 160},
                {"date": "14:00", "volume": 90},
                {"date": "16:00", "volume": 140},
                {"date": "18:00", "volume": 190},
            ],
            insights=[
                "Peak traffic detected between 5:00 PM and 7:00 PM.",
                "Coke Zero stocks are critically low (3 units left).",
            ],
            coach_message="Traffic is surging in the late afternoon. Consider moving high-margin snacks near the counter for the 5 PM rush."
        )
