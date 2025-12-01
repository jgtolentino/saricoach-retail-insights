from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import store, coach

app = FastAPI(title="SariCoach API")

# CRITICAL: Allow your Vercel frontend to talk to this backend
origins = [
    "https://agents-intensive-saricoach.vercel.app",
    "https://saricoach-retail-insights.vercel.app",
    "http://localhost:5173",
    "*" # Temporarily allow all for debugging
]

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
