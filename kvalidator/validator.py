from __future__ import annotations

import math
from typing import Any


class StreamSchemaValidator:
    """Strict Kafka event payload validator for order schemas."""

    def validate_order(self, payload: dict[str, Any]) -> tuple[bool, str]:
        required = ("order_id", "amount", "user_id")
        for field in required:
            if field not in payload:
                return False, f"Missing required field: {field}"

        for str_field in ("order_id", "user_id"):
            val = payload[str_field]
            if not isinstance(val, str) or not val.strip():
                return False, f"Field '{str_field}' must be a non-empty string"

        amount = payload["amount"]
        if (
            isinstance(amount, bool)
            or not isinstance(amount, int | float)
            or not math.isfinite(amount)
            or amount <= 0
        ):
            return False, "Amount must be a finite positive number"

        return True, "Valid"
