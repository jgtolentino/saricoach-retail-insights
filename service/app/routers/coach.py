import os
import google.generativeai as genai
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..deps import get_backend
from ..backend.base import DataBackend
from ..config import settings

router = APIRouter(tags=["coach"])

class CoachRequest(BaseModel):
    store_id: int
    question: str

# Initialize Gemini
genai.configure(api_key=settings.google_api_key)

@router.post("/coach/ask")
def ask_coach(payload: CoachRequest, backend: DataBackend = Depends(get_backend)):
    # 1. Fetch Real Data
    summary = backend.fetch_store_summary(payload.store_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Store data not available for context.")

    # 2. Construct Data Context (The "RAG" part)
    # We turn the JSON object into a readable text summary for the LLM
    kpi_text = "\n".join([f"- {k.label}: {k.value} ({k.trend})" for k in summary.kpis])
    insights_text = "\n".join([f"- {i}" for i in summary.insights])
    
    system_instruction = f"""
    You are SariCoach, an expert retail consultant for a Sari-Sari store in the Philippines.
    
    CURRENT STORE STATUS (Today):
    {kpi_text}
    
    RECENT AUTOMATED ALERTS:
    {insights_text}
    
    INSTRUCTIONS:
    - Answer the user's question using the data above.
    - Be specific. If they ask "How is sales?", quote the exact Revenue number.
    - Keep answers short, encouraging, and actionable.
    - If the data is bad (downward trends), suggest a fix.
    """

    try:
        # 3. Call Gemini
        # using gemini-flash-latest as verified by list_models.py
        model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)
        
        response = model.generate_content(payload.question)
        return {"answer": response.text}

    except Exception as e:
        print(f"Gemini Error: {e}")
        raise HTTPException(status_code=500, detail="Coach is currently offline.")
