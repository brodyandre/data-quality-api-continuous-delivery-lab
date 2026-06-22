import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_healthy_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_version_endpoint_returns_app_metadata(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("APP_VERSION", "1.2.3")

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "app_name": "data-quality-api",
        "app_version": "1.2.3",
        "environment": "staging",
    }


def test_environment_endpoint_returns_expected_variables(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.setenv("QUALITY_THRESHOLD", "94")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    response = client.get("/environment")

    assert response.status_code == 200
    assert response.json() == {
        "environment": "staging",
        "quality_threshold": 94,
        "log_level": "debug",
    }


def test_quality_report_returns_expected_fields(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("QUALITY_THRESHOLD", "95")

    response = client.get("/quality-report")
    payload = response.json()

    assert response.status_code == 200
    assert payload["environment"] == "production"
    assert payload["pipeline_status"] == "success"
    assert payload["quality_score"] == 96.4
    assert payload["threshold"] == 95
    assert payload["passed"] is True


def test_quality_threshold_influences_passed_field(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("QUALITY_THRESHOLD", "97")

    response = client.get("/quality-report")
    payload = response.json()

    assert response.status_code == 200
    assert payload["threshold"] == 97
    assert payload["passed"] is False
    assert isinstance(payload["checked_at"], str)
