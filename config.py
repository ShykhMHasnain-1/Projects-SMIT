"""
Configuration settings for AI Smart Civic Services.
"""
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    # Core Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "civic-sense-ai-super-secret-key-2026")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Database
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "database", "civic.db")
    )

    # Uploads
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads")
    )
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Sessions
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # AI Model
    AI_MODEL_DIR = os.environ.get("AI_MODEL_DIR", os.path.join(BASE_DIR, "backend", "ai_model"))

    # Escalation
    CRITICAL_ESCALATION_HOURS = int(os.environ.get("CRITICAL_ESCALATION_HOURS", "4"))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
