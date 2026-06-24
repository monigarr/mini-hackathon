# ============================================================================
# Module: config.py
# Purpose: Environment configuration helpers
# Owner: Monica Peters
# Last Updated: 2026-06-24
# License: MIT
# ============================================================================

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    environment: str = getenv("ENVIRONMENT", "development")
    openai_api_key: str | None = getenv("OPENAI_API_KEY")
    port: int = int(getenv("PORT", "8000"))


settings = Settings()

