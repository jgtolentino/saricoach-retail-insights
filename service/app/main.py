from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import store, coach

app = FastAPI(title="SariCoach API")

import os

# Allow frontend to talk to backend
origins = os.getenv("SARICOACH_CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(store.router, prefix="/api")
app.include_router(coach.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
