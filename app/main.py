from typing import Any

from fastapi import FastAPI

from app.schemas import (
    HealthResponse,
    MissingFieldSummary,
    QualityCheckRequest,
    QualityCheckResponse,
)
from app.settings import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Simple API used to demonstrate continuous delivery workflows.",
)


def is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Data Quality API is running.",
        "environment": settings.app_env,
        "docs_url": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.app_env,
        version=settings.app_version,
    )


@app.post("/quality/check", response_model=QualityCheckResponse)
def quality_check(payload: QualityCheckRequest) -> QualityCheckResponse:
    threshold = (
        payload.null_threshold
        if payload.null_threshold is not None
        else settings.default_null_threshold
    )
    total_records = len(payload.records)
    missing_fields: list[MissingFieldSummary] = []

    for field in payload.required_fields:
        missing_count = sum(1 for record in payload.records if is_missing(record.get(field)))
        missing_ratio = (missing_count / total_records) if total_records else 0.0
        missing_fields.append(
            MissingFieldSummary(
                field=field,
                missing_count=missing_count,
                missing_ratio=round(missing_ratio, 4),
            )
        )

    is_valid = all(item.missing_ratio <= threshold for item in missing_fields)

    return QualityCheckResponse(
        total_records=total_records,
        required_fields=payload.required_fields,
        null_threshold=threshold,
        missing_fields=missing_fields,
        is_valid=is_valid,
    )
