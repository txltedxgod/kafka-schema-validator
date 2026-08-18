from kvalidator.validator import StreamSchemaValidator

def test_validation():
    v = StreamSchemaValidator()
    ok, _ = v.validate_order({"order_id": "1", "amount": 100.0, "user_id": "u1"})
    assert ok is True
