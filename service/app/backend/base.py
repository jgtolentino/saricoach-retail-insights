from abc import ABC, abstractmethod
from typing import Optional
from ..models import StoreSummary

class DataBackend(ABC):
    @abstractmethod
    def fetch_store_summary(self, store_id: int) -> Optional[StoreSummary]:
        pass
