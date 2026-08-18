from typing import Dict, Any, Tuple

class StreamSchemaValidator:
    def validate_order(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        required = ["order_id", "amount", "user_id"]
        for r in required:
            if r not in payload:
                return False, f"Missing required field: {r}"
        if not isinstance(payload["amount"], (int, float)) or payload["amount"] <= 0:
            return False, "Amount must be a positive number"
        return True, "Valid"
