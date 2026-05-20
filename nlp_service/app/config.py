from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # ===============================
    # 🌍 ENVIRONMENT
    # ===============================
    ENV: str = Field(default="production")

    # ===============================
    # 🔴 REDIS (CELERY)
    # ===============================
    REDIS_BROKER_URL: str = Field(..., description="Redis broker URL")
    REDIS_BACKEND_URL: str = Field(..., description="Redis backend URL")

    # ===============================
    # 🍃 MONGODB
    # ===============================
    MONGO_URI: str = Field(..., description="MongoDB connection URI")
    MONGO_DB: str = Field(default="solvelitigation")
    JUDGMENTS_COLLECTION: str = Field(default="judgments")

    # ===============================
    # ⚡ FASTAPI SERVER
    # ===============================
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # ===============================
    # 🔗 BACKEND CALLBACK
    # ===============================
    BACKEND_CALLBACK_URL: str = Field(
        ..., description="Backend NLP callback URL"
    )

    # ===============================
    # 📂 UPLOAD DIRECTORY
    # ===============================
    UPLOAD_BASE_DIR: str = Field(
        ..., description="Base directory for uploaded PDFs"
    )

    # ===============================
    # 🧠 SERVICE NAME
    # ===============================
    NLP_SERVICE_NAME: str = Field(default="nlp_service")

    # ===============================
    # 🔐 OPTIONAL ENV (SAFE ADDITIONS)
    # ===============================
    nlp_internal_key: str | None = None
    ingestion_collection: str | None = None

    # ===============================
    # 🔥 FINAL CONFIG (CRITICAL FIX)
    # ===============================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"   # ✅ allows unknown env vars (fixes your crash)
    )


# ===============================
# 🚀 LOAD SETTINGS
# ===============================
settings = Settings()
