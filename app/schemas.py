from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class VersionResponse(BaseModel):
    app_name: str
    app_version: str
    environment: str


class EnvironmentResponse(BaseModel):
    environment: str
    quality_threshold: int
    log_level: str


class QualityReportResponse(BaseModel):
    environment: str
    pipeline_status: str
    records_processed: int = Field(ge=0)
    quality_score: float = Field(ge=0, le=100)
    threshold: int = Field(ge=0, le=100)
    passed: bool
    checked_at: datetime
