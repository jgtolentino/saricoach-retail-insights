from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple, Union
import pandas as pd

@dataclass
class DataContext:
    """
    Holds all canonical SariCoach DataFrames.
    Expects the same structure as data/processed/*.csv.
    """
    brands: pd.DataFrame
    products: pd.DataFrame
    stores: pd.DataFrame
    transactions: pd.DataFrame
    transaction_lines: pd.DataFrame
    shelf_vision: pd.DataFrame
    stt_events: pd.DataFrame
    weather: pd.DataFrame
    foot_traffic: pd.DataFrame

    @classmethod
    def from_folder(cls, base_path: Union[str, "os.PathLike[str]"]) -> "DataContext":
        # This will be implemented by the CSV backend, but we keep the type here.
        raise NotImplementedError("Use saricoach.backends.csv_backend.build_context_from_csv")
