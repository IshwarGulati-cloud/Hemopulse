import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "HemoPulse Backend API"
    API_V1_STR: str = "/api/v1"
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = Field(
        default_factory=lambda: os.getenv("SUPABASE_ANON_KEY", ""),
        validation_alias="SUPABASE_ANON_KEY",
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
