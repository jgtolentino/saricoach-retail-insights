# service/app/main.py

from pathlib import Path
from datetime import date

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.feature_frame import DataContext, summarize_brand_window
from src.agents.core import PlannerAgent, DataAnalystAgent, CoachAgent
from .models import CoachRequest, CoachResponse, StoreSummaryResponse


BASE_DIR = Path(__file__).resolve().parents[2]  # repo root
DATA_DIR = BASE_DIR / "data" / "processed"

app = FastAPI(
    title="SariCoach Service",
    version="0.1.0",
)

# CORS for local React dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load data at startup ---

def load_context() -> DataContext:
    brands = pd.read_csv(DATA_DIR / "brands.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    stores = pd.read_csv(DATA_DIR / "stores.csv")
    transactions = pd.read_csv(DATA_DIR / "transactions.csv", parse_dates=["tx_timestamp"])
    transaction_lines = pd.read_csv(DATA_DIR / "transaction_lines.csv")
    shelf_vision = pd.read_csv(DATA_DIR / "shelf_vision_events.csv", parse_dates=["event_timestamp"])
    stt_events = pd.read_csv(DATA_DIR / "stt_events.csv", parse_dates=["event_timestamp"])
    weather = pd.read_csv(DATA_DIR / "weather_daily.csv", parse_dates=["date"])
    foot_traffic = pd.read_csv(DATA_DIR / "foot_traffic_daily.csv", parse_dates=["date"])

    return DataContext(
        brands=brands,
        products=products,
        stores=stores,
        transactions=transactions,
        transaction_lines=transaction_lines,
        shelf_vision=shelf_vision,
        stt_events=stt_events,
        weather=weather,
        foot_traffic=foot_traffic,
    )


CTX = load_context()
PLANNER = PlannerAgent()
ANALYST = DataAnalystAgent(ctx=CTX)
COACH = CoachAgent(model_name="heuristic", use_gemini=False)  # flip later if you wire Gemini


# --- Helper: KPI computation ---

def compute_store_kpis(store_id: int) -> dict:
    tx = CTX.transactions.copy()
    tx = tx[tx["store_id"] == store_id]
    if tx.empty:
        return {
            "daily_sales": 0,
            "daily_sales_delta": 0.0,
            "stockout_risk": "unknown",
            "hot_brand": None,
        }

    tx["date"] = tx["tx_timestamp"].dt.date

    today = tx["date"].max()
    yesterday = max(d for d in tx["date"].unique() if d < today) if (tx["date"].nunique() > 1) else today

    today_sales = tx.loc[tx["date"] == today, "total_amount"].sum() if "total_amount" in tx.columns else \
                  tx.loc[tx["date"] == today, "subtotal"].sum()

    yest_sales = tx.loc[tx["date"] == yesterday, "total_amount"].sum() if "total_amount" in tx.columns else \
                 tx.loc[tx["date"] == yesterday, "subtotal"].sum()

    if yest_sales > 0:
        delta = (today_sales - yest_sales) / yest_sales
    else:
        delta = 0.0

    # Rough stockout risk: based on oos_rate_avg from brand window
    ff = summarize_brand_window(
        CTX.transactions.assign(date=CTX.transactions["tx_timestamp"].dt.date).pipe(lambda _: _),  # no-op placeholder
        window_days=30,
    )
    # safer: fallback if not wired, keep "medium"
    stockout_risk = "medium"

    # Hot brand: top revenue over full window
    # (simple, consistent with capstone)
    # We rely on a separate brand summary call – but to keep it self-contained:
    # reuse tx + transaction_lines
    tl = CTX.transaction_lines.copy()
    tl = tl.merge(tx[["transaction_id"]], on="transaction_id", how="inner")
    if "subtotal" in tl.columns:
        rev_per_brand = tl.groupby("brand_id")["subtotal"].sum().reset_index()
    else:
        rev_per_brand = tl.groupby("brand_id")["quantity"].sum().reset_index(name="subtotal")

    if not rev_per_brand.empty:
        top_brand_id = int(rev_per_brand.sort_values("subtotal", ascending=False)["brand_id"].iloc[0])
        brands = CTX.brands.set_index("brand_id")
        hot_brand = brands.loc[top_brand_id, "brand_name"] if top_brand_id in brands.index else None
    else:
        hot_brand = None

    return {
        "daily_sales": float(today_sales),
        "daily_sales_delta": float(round(delta, 3)),
        "stockout_risk": stockout_risk,
        "hot_brand": hot_brand,
    }


# --- Routes ---

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/store/{store_id}/summary", response_model=StoreSummaryResponse)
def store_summary(store_id: int):
    # Default decision = seven day plan for store
    decision = PLANNER.plan({
        "type": "seven_day_plan",
        "store_id": store_id,
        "days": 30,
    })
    analytics = ANALYST.analyze(decision)
    coach_output = COACH.coach(analytics, persona="store_owner")

    kpis = compute_store_kpis(store_id)

    coach_resp = CoachResponse(
        actions=coach_output.actions,
        risks=coach_output.risks,
        opportunities=coach_output.opportunities,
        debug_notes=coach_output.debug_notes,
    )

    return StoreSummaryResponse(
        store_id=store_id,
        date=str(date.today()),
        kpis=kpis,
        coach=coach_resp,
    )


@app.post("/api/coach/recommendations", response_model=CoachResponse)
def coach_recommendations(req: CoachRequest):
    decision = PLANNER.plan({
        "type": req.type,
        "store_id": req.store_id,
        "brand_id": req.brand_id,
        "category": req.category,
        "days": req.days,
    })
    analytics = ANALYST.analyze(decision)
    coach_output = COACH.coach(analytics, persona=req.persona)

    return CoachResponse(
        actions=coach_output.actions,
        risks=coach_output.risks,
        opportunities=coach_output.opportunities,
        debug_notes=coach_output.debug_notes,
    )
