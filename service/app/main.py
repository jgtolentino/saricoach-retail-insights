from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import health, store, coach

app = FastAPI(title="SariCoach API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(store.router)
app.include_router(coach.router)
