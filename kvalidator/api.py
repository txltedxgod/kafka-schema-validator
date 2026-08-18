from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any
from kvalidator.validator import StreamSchemaValidator

app = FastAPI(title="Kafka Schema Validator", version="0.1.0")
v = StreamSchemaValidator()

class PayloadReq(BaseModel):
    topic: str
    data: Dict[str, Any]

@app.post("/api/v1/validate")
def validate(req: PayloadReq):
    ok, reason = v.validate_order(req.data)
    target = req.topic if ok else f"{req.topic}.DLQ"
    return {"valid": ok, "target_topic": target, "message": reason}
