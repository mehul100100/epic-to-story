import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER")
    VERIFY_STORIES: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()