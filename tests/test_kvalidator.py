from fastapi.testclient import TestClient

from kvalidator.api import app
from kvalidator.validator import StreamSchemaValidator

client = TestClient(app)


def test_validation() -> None:
    v = StreamSchemaValidator()
    ok, reason = v.validate_order({"order_id": "1", "amount": 100.0, "user_id": "u1"})
    assert ok is True
    assert reason == "Valid"


def test_validation_rejects_bool_nan_and_blank_fields() -> None:
    v = StreamSchemaValidator()
    assert v.validate_order({"order_id": "1", "amount": True, "user_id": "u1"})[0] is False
    assert v.validate_order({"order_id": "1", "amount": float("nan"), "user_id": "u1"})[0] is False
    assert v.validate_order({"order_id": "1", "amount": float("inf"), "user_id": "u1"})[0] is False
    assert v.validate_order({"order_id": "  ", "amount": 10.0, "user_id": "u1"})[0] is False
    assert v.validate_order({"order_id": "1", "amount": 10.0}) == (
        False,
        "Missing required field: user_id",
    )


def test_validator_api_routes_to_dlq_on_invalid_payload() -> None:
    assert client.get("/health").json() == {"status": "ok"}

    ok_resp = client.post(
        "/api/v1/validate",
        json={
            "topic": "orders.created",
            "data": {"order_id": "ord-9", "amount": 49.99, "user_id": "usr-1"},
        },
    )
    assert ok_resp.status_code == 200
    assert ok_resp.json()["valid"] is True
    assert ok_resp.json()["target_topic"] == "orders.created"

    bad_resp = client.post(
        "/api/v1/validate",
        json={
            "topic": "orders.created",
            "data": {"order_id": "ord-9", "amount": True, "user_id": "usr-1"},
        },
    )
    assert bad_resp.status_code == 200
    assert bad_resp.json()["valid"] is False
    assert bad_resp.json()["target_topic"] == "orders.created.DLQ"

    bad_topic = client.post(
        "/api/v1/validate",
        json={"topic": "bad topic", "data": {}},
    )
    assert bad_topic.status_code == 400
