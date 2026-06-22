from datetime import datetime, timezone

from fastapi import FastAPI

from app.schemas import (
    EnvironmentResponse,
    HealthResponse,
    QualityReportResponse,
    VersionResponse,
)
from app.settings import Settings, get_settings

app = FastAPI(
    title="data-quality-api",
    version="0.1.0",
    description="Simple API used to demonstrate continuous delivery workflows.",
)


def build_quality_report(
    settings: Settings, checked_at: datetime | None = None
) -> QualityReportResponse:
    report_checked_at = checked_at or datetime.now(timezone.utc)
    quality_score = 96.4
    records_processed = 125000

    return QualityReportResponse(
        environment=settings.app_env,
        pipeline_status="success",
        records_processed=records_processed,
        quality_score=quality_score,
        threshold=settings.quality_threshold,
        passed=quality_score >= settings.quality_threshold,
        checked_at=report_checked_at,
    )


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/version", response_model=VersionResponse)
def get_version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )


@app.get("/environment", response_model=EnvironmentResponse)
def get_environment() -> EnvironmentResponse:
    settings = get_settings()
    return EnvironmentResponse(
        app_env=settings.app_env,
        app_version=settings.app_version,
        quality_threshold=settings.quality_threshold,
        log_level=settings.log_level,
    )


@app.get("/quality-report", response_model=QualityReportResponse)
def get_quality_report() -> QualityReportResponse:
    return build_quality_report(get_settings())
