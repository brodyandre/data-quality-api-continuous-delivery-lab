from datetime import datetime, timezone
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import build_quality_report, get_environment, get_version, health_check
from app.settings import Settings


def test_health_endpoint_returns_ok() -> None:
    response = health_check()

    assert response.model_dump() == {"status": "ok"}


def test_version_endpoint_uses_default_settings(monkeypatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("APP_VERSION", raising=False)

    response = get_version()

    assert response.model_dump() == {
        "application": "data-quality-api",
        "version": "0.1.0",
        "environment": "local",
    }


def test_environment_endpoint_returns_expected_variables(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("APP_VERSION", "1.2.3")
    monkeypatch.setenv("QUALITY_THRESHOLD", "94")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    response = get_environment()

    assert response.model_dump() == {
        "app_env": "staging",
        "app_version": "1.2.3",
        "quality_threshold": 94,
        "log_level": "debug",
    }


def test_quality_report_uses_threshold_to_define_passed_status() -> None:
    checked_at = datetime(2026, 6, 22, 12, 0, tzinfo=timezone.utc)
    settings = Settings(
        app_env="production",
        app_version="2.0.0",
        quality_threshold=97,
        log_level="info",
    )

    response = build_quality_report(settings, checked_at=checked_at)

    assert response.model_dump() == {
        "environment": "production",
        "pipeline_status": "success",
        "records_processed": 125000,
        "quality_score": 96.4,
        "threshold": 97,
        "passed": False,
        "checked_at": checked_at,
    }
