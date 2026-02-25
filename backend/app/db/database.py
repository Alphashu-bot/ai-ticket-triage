"""
Database engine, session, and base model configuration.
Uses SQLAlchemy async-compatible patterns with SQLite as the default backend.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config.settings import settings

# ---------------------------------------------------------------------------
# Engine & Session
# ---------------------------------------------------------------------------
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------------------------
# Declarative Base
# ---------------------------------------------------------------------------
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session and ensures
    it is closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables defined by ORM models."""
    Base.metadata.create_all(bind=engine)
