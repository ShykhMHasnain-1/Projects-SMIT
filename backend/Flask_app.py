"""
Configuration for AI Smart Civic Services.
All secrets are read from environment variables — nothing sensitive is hard-coded.
Copy .env.example to .env and fill in real values before deploying.
"""
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    # --- Core Flask ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

    # --- Database ---
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "database", "civic.db")
    )
    # NOTE: DatabaseManager only talks to SQLite through parameterized SQL.
    # To migrate to PostgreSQL/MySQL, swap DatabaseManager's connection layer
    # for SQLAlchemy/psycopg2 — the rest of the app talks to DatabaseManager's
    # methods only, never to raw SQL, so the migration is isolated.

    # --- Uploads ---
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads")
    )
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB max upload
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # --- Sessions ---
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # --- AI ---
    AI_MODEL_DIR = os.environ.get("AI_MODEL_DIR", os.path.join(BASE_DIR, "ai"))
    # Optional: if an external LLM API key is provided, AIAnalyzer can use it
    # for richer summarization. Never required — the app is fully functional
    # with the local scikit-learn pipeline if this is absent.
    EXTERNAL_AI_API_KEY = os.environ.get("EXTERNAL_AI_API_KEY", "")

    # --- Escalation ---
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