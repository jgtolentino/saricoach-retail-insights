import subprocess
import sys
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

def test_seed_script_generates_processed_files(tmp_path, monkeypatch):
    repo_root = ROOT
    data_dir = repo_root / "data"
    
    # We'll use the actual data dir since the script hardcodes paths relative to CWD
    # But we can check if files exist after run
    
    processed_dir = data_dir / "processed"
    
    # Precondition: script exists
    script = repo_root / "seed_saricoach_data.py"
    assert script.exists(), "seed_saricoach_data.py missing"
    
    # Run the script using the same python executable
    subprocess.check_call([sys.executable, str(script)], cwd=repo_root)
    
    expected = [
        "brands.csv",
        "products.csv",
        "stores.csv",
        "transactions.csv",
        "transaction_lines.csv",
        "shelf_vision_events.csv",
        "stt_events.csv",
        "weather_daily.csv",
        "foot_traffic_daily.csv",
    ]
    
    for fname in expected:
        path = processed_dir / fname
        assert path.exists(), f"{fname} not generated"
        
    # Basic sanity: transactions must have a store_id and timestamp
    tx = pd.read_csv(processed_dir / "transactions.csv")
    assert "store_id" in tx.columns
    assert any(col for col in tx.columns if "time" in col.lower())
