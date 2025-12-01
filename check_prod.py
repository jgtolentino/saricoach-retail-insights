import requests
import sys
import os

# Default to localhost for testing, but allow override
API_URL = os.getenv("API_URL", "http://localhost:8000")
STORE_ID = 1

def run_tests():
    print(f"🚀 Testing Production at {API_URL}...")

    # 1. Health Check
    try:
        health = requests.get(f"{API_URL}/api/health", timeout=5)
        if health.status_code == 200:
            print("✅ Health Check: OK")
        else:
            print(f"❌ Health Check Failed: {health.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        sys.exit(1)

    # 2. Database/Data Check
    try:
        summary = requests.get(f"{API_URL}/api/store/{STORE_ID}/summary", timeout=5)
        if summary.status_code == 200:
            data = summary.json()
            if "store_name" in data and len(data["kpis"]) > 0:
                print(f"✅ Data Fetch: OK (Store: {data['store_name']})")
            else:
                print("⚠️ Data Fetch: OK but content empty")
        else:
            print(f"❌ Data Fetch Failed: {summary.status_code}")
    except Exception as e:
        print(f"❌ Data Fetch Error: {e}")

    # 3. AI Agent Check (Optional - costs money/quota)
    # prompt = {"question": "Ping"}
    # ... request to /api/coach/ask ...
    
    print("✨ System Ready for Demo.")

if __name__ == "__main__":
    run_tests()
