from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Data Quality API"
    app_env: str = "development"
    app_version: str = "0.1.0"
    default_null_threshold: float = 0.2

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_name=os.getenv("APP_NAME", cls.app_name),
            app_env=os.getenv("APP_ENV", cls.app_env),
            app_version=os.getenv("APP_VERSION", cls.app_version),
            default_null_threshold=float(
                os.getenv("DEFAULT_NULL_THRESHOLD", cls.default_null_threshold)
            ),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
