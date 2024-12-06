from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Cache settings for better performance."""
    return Settings()
