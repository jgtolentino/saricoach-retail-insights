from fastapi import APIRouter, Depends, HTTPException
from ..deps import get_backend
from ..backend.base import DataBackend
from ..models import StoreSummary

router = APIRouter(tags=["store"])

@router.get("/store/{store_id}/summary", response_model=StoreSummary)
def get_store_summary(store_id: int, backend: DataBackend = Depends(get_backend)):
    summary = backend.fetch_store_summary(store_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Store not found")
    return summary
