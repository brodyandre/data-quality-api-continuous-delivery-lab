import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "data-quality-api"
    app_env: str = "local"
    app_version: str = "0.1.0"
    quality_threshold: int = 90
    log_level: str = "info"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            app_env=os.getenv("APP_ENV", cls.app_env),
            app_version=os.getenv("APP_VERSION", cls.app_version),
            quality_threshold=int(
                os.getenv("QUALITY_THRESHOLD", str(cls.quality_threshold))
            ),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
        )


def get_settings() -> Settings:
    return Settings.from_env()
