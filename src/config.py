from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global config for SariCoach."""

    google_api_key: str = ""
    google_model: str = "gemini-1.5-pro"

    # analysis windows / thresholds
    window_days: int = 30

    class Config:
        env_prefix = "SARICOACH_"
