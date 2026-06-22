from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    environment: str
    version: str


class MissingFieldSummary(BaseModel):
    field: str
    missing_count: int
    missing_ratio: float


class QualityCheckRequest(BaseModel):
    records: list[dict[str, Any]]
    required_fields: list[str] = Field(default_factory=list)
    null_threshold: float | None = Field(default=None, ge=0.0, le=1.0)


class QualityCheckResponse(BaseModel):
    total_records: int
    required_fields: list[str]
    null_threshold: float
    missing_fields: list[MissingFieldSummary]
    is_valid: bool
