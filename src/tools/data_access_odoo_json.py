from typing import Any, Dict, List


class PayloadValidationError(ValueError):
    pass


REQUIRED_KEYS = ["store", "transactions"]


def validate_payload(payload: Dict[str, Any]) -> None:
    missing = [k for k in REQUIRED_KEYS if k not in payload]
    if missing:
        raise PayloadValidationError(f"Missing keys in payload: {missing}")


def get_store(payload: Dict[str, Any]) -> Dict[str, Any]:
    validate_payload(payload)
    return payload["store"]


def get_transactions(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    validate_payload(payload)
    return payload.get("transactions", [])
