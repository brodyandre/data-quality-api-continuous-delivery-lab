import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import health_check, quality_check, read_root
from app.schemas import QualityCheckRequest


def test_root_endpoint_returns_basic_metadata() -> None:
    response = read_root()

    assert response["environment"] == "development"


def test_health_endpoint_returns_ok() -> None:
    response = health_check()

    assert response.model_dump() == {
        "status": "ok",
        "environment": "development",
        "version": "0.1.0",
    }


def test_quality_check_flags_missing_required_fields() -> None:
    payload = QualityCheckRequest(
        records=[
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "", "email": "bob@example.com"},
            {"id": 3, "email": "carol@example.com"},
        ],
        required_fields=["name", "email"],
        null_threshold=0.2,
    )

    response = quality_check(payload)

    assert response.is_valid is False
    assert [item.model_dump() for item in response.missing_fields] == [
        {"field": "name", "missing_count": 2, "missing_ratio": 0.6667},
        {"field": "email", "missing_count": 0, "missing_ratio": 0.0},
    ]


def test_quality_check_accepts_complete_payload() -> None:
    payload = QualityCheckRequest(
        records=[
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ],
        required_fields=["name", "email"],
    )

    response = quality_check(payload)

    assert response.is_valid is True
