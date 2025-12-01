# API Documentation

Base URL: `http://localhost:8000`

## Endpoints

### Health Check
- **GET** `/api/health`
- **Response**: `{"status": "ok"}`

### Store Summary
- **GET** `/api/store/{store_id}/summary`
- **Description**: Returns high-level KPIs and coach suggestions for a store.
- **Response**:
  ```json
  {
    "store_id": 1,
    "date": "2024-01-01",
    "kpis": {
      "daily_sales": 1234.5,
      "daily_sales_delta": 0.05,
      "stockout_risk": "low",
      "hot_brand": "Brand A"
    },
    "coach": {
      "actions": ["Restock Brand A"],
      "risks": [],
      "opportunities": ["Promote Brand B"],
      "debug_notes": {}
    }
  }
  ```

### Coach Recommendations
- **POST** `/api/coach/recommendations`
- **Description**: Get specific recommendations based on parameters.
- **Payload**:
  ```json
  {
    "store_id": 1,
    "type": "seven_day_plan",
    "brand_id": null,
    "category": null,
    "days": 30,
    "persona": "store_owner"
  }
  ```
- **Response**: Same `CoachResponse` structure as in Store Summary.
