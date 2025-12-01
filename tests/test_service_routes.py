from fastapi.testclient import TestClient
from service.app.main import app
import pytest

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_store_summary_basic():
    # Assuming store 1 exists from seed data
    res = client.get("/api/store/1/summary")
    
    # If this fails with 500, it catches the bug we saw earlier
    assert res.status_code == 200

    data = res.json()
    assert data["store_id"] == 1
    assert "kpis" in data
    assert "coach" in data

    kpis = data["kpis"]
    assert "daily_sales" in kpis
    # stockout_risk might be "unknown" or "medium" depending on logic
    assert "stockout_risk" in kpis

    coach = data["coach"]
    assert isinstance(coach["actions"], list)
    assert isinstance(coach["risks"], list)
    assert isinstance(coach["opportunities"], list)
