from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from kvalidator.validator import StreamSchemaValidator

app = FastAPI(title="Kafka Schema Validator", version="0.1.0")
v = StreamSchemaValidator()


class PayloadReq(BaseModel):
    topic: str = Field(..., min_length=1)
    data: dict[str, Any]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/validate")
def validate(req: PayloadReq) -> dict[str, object]:
    topic = req.topic.strip()
    if not topic or any(ch.isspace() for ch in topic):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="topic must be a non-empty identifier without whitespace",
        )
    ok, reason = v.validate_order(req.data)
    target = topic if ok else f"{topic}.DLQ"
    return {"valid": ok, "target_topic": target, "message": reason}
