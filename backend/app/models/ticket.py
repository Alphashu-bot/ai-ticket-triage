"""
SQLAlchemy ORM model for support tickets.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text

from app.db.database import Base


class Ticket(Base):
    """Represents an analyzed support ticket stored in the database."""

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(10), nullable=False)
    urgency = Column(Boolean, default=False)
    keywords = Column(Text, nullable=False)          # Stored as comma-separated string
    confidence = Column(Float, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<Ticket(id={self.id}, category='{self.category}', "
            f"priority='{self.priority}')>"
        )
