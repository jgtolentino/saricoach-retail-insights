import pytest
import pandas as pd
from saricoach.feature_frame import build_brand_day_frame, summarize_brand_window
from saricoach.data_context import DataContext

# Mock DataContext fixture
@pytest.fixture
def mock_ctx():
    # Minimal mock data
    dates = pd.date_range("2024-01-01", periods=5)
    brands = pd.DataFrame({"brand_id": [1, 2], "brand_name": ["A", "B"], "category": ["Cat1", "Cat2"]})
    stores = pd.DataFrame({"store_id": [1]})
    
    # Transactions
    tx = pd.DataFrame({
        "transaction_id": range(10),
        "store_id": [1]*10,
        "tx_timestamp": dates.repeat(2),
    })
    tl = pd.DataFrame({
        "transaction_id": range(10),
        "brand_id": [1, 2]*5,
        "quantity": [1]*10,
        "subtotal": [10.0]*10,
    })
    
    # Empty other tables for simplicity
    empty = pd.DataFrame()
    weather = pd.DataFrame({"date": dates, "store_id": 1, "temp_c": 25, "rainfall_mm": 0, "condition": "Sunny"})
    traffic = pd.DataFrame({"date": dates, "store_id": 1, "traffic_index": 100})
    
    return DataContext(
        brands=brands, products=empty, stores=stores,
        transactions=tx, transaction_lines=tl,
        shelf_vision=pd.DataFrame(columns=["event_timestamp", "store_id", "brand_id", "facings", "share_of_shelf", "oos_flag"]),
        stt_events=pd.DataFrame(columns=["event_timestamp", "store_id", "brand_id", "id", "sentiment_score", "intent_label"]),
        weather=weather, foot_traffic=traffic
    )

def test_build_feature_frame(mock_ctx):
    ff = build_brand_day_frame(mock_ctx, store_id=1)
    assert not ff.empty
    assert "date" in ff.columns
    assert "brand_id" in ff.columns
    assert "revenue" in ff.columns
    # Check aggregation
    assert ff["qty_sold"].sum() == 10

def test_summarize_brand_window(mock_ctx):
    ff = build_brand_day_frame(mock_ctx, store_id=1)
    summary = summarize_brand_window(ff, window_days=30)
    assert not summary.empty
    assert "brand_name" in summary.columns
    assert len(summary) == 2 # 2 brands
