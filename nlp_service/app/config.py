from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Environment
    ENV: str = Field(default="production")

    # Redis (Celery)
    REDIS_BROKER_URL: str = Field(..., description="Redis broker URL")
    REDIS_BACKEND_URL: str = Field(..., description="Redis backend URL")

    # MongoDB
    MONGO_URI: str = Field(..., description="MongoDB connection URI")
    MONGO_DB: str = Field(default="solvelitigation")
    JUDGMENTS_COLLECTION: str = Field(default="judgments")

    # FastAPI
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # Backend callback
    BACKEND_CALLBACK_URL: str = Field(
        ..., description="Backend NLP callback URL"
    )

    # Service name
    NLP_SERVICE_NAME: str = Field(default="nlp_service")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # explicitly forbid unknown keys


# Singleton
settings = Settings()
