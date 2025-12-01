from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    data_backend: str = "csv"  # or "supabase"
    database_url: Optional[str] = None
    google_api_key: Optional[str] = None
    
    class Config:
        env_prefix = "SARICOACH_"
        env_file = (".env", ".env.local")
        extra = "ignore"

settings = Settings()
