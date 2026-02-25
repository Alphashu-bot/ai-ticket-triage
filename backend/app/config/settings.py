"""
Application configuration settings.
Uses environment variables with sensible defaults for local development.
"""

import os


class Settings:
    """Centralized application configuration."""

    # Application metadata
    APP_NAME: str = "AI Ticket Triage"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./tickets.db"
    )

    # CORS settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",   # Alternative frontend port
        "http://frontend:5173",   # Docker service name
    ]


settings = Settings()
