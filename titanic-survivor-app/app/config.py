from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from functools import lru_cache

from app import model_version
from app.log_config import app_config


logger = app_config.get_logger()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    # e.g: http://localhost,http://localhost:4200,http://localhost:3000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8000",  # type: ignore
    ]

    PROJECT_NAME: str = "Titanic Survivor Service"
    TRAINED_MODEL_NAME: str = model_version + ".pkl"

    class Config:
        case_sensitive = True


@lru_cache
def get_settings():
    logger.info("Getting the app settings...")
    return Settings()
