from pydantic_settings import BaseSettings
from typing import List, ClassVar, Dict
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # FastAPI Config
    app_name: str = "SMB02 Outreach Engine"
    app_version: str = "1.0.0"
    fastapi_env: str = os.getenv("FASTAPI_ENV", "development")
    api_port: int = int(os.getenv("API_PORT", 8000))
    api_host: str = os.getenv("API_HOST", "0.0.0.0")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # MongoDB
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_db: str = os.getenv("MONGODB_DB", "smb02_db")
    mongodb_user: str = os.getenv("MONGODB_USER", "root")
    mongodb_password: str = os.getenv("MONGODB_PASSWORD", "password")

    # Hugging Face
    hf_token: str = os.getenv("HF_TOKEN", "")
    model_name: str = os.getenv("MODEL_NAME", "QuantFactory/BitNet-3B-1.58-nf4")
    model_cache_dir: str = os.getenv("MODEL_CACHE_DIR", "./models_cache")

    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:8000")
    cors_origins: List[str] = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000"
    ]

    # Memory
    memory_dir: str = os.getenv("MEMORY_DIR", "./memory")

    # API Config
    apify_api_token: str = os.getenv("APIFY_API_TOKEN", "")

    # Subscription Plans (IMPORTANT FIX)
    plan_limits: ClassVar[Dict[str, int]] = {
        "FREE": 3,
        "PRO": 200,
        "ULTRA": 1000,
        "BUSINESS": 999999
    }

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
