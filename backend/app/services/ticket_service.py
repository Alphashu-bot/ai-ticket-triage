"""
Business logic layer for ticket operations.

The service layer sits between the controller and the data / analyzer layers,
orchestrating analysis and persistence without coupling to HTTP concerns.
"""

from sqlalchemy.orm import Session

from app.analyzer.nlp_engine import analyze_ticket, AnalysisResult
from app.models.ticket import Ticket


def analyze_and_store_ticket(message: str, db: Session) -> Ticket:
    """
    Analyze a raw message and persist the result to the database.

    Args:
        message: The support ticket text submitted by the user.
        db: Active SQLAlchemy session.

    Returns:
        The newly created Ticket ORM instance (with generated id).
    """
    result: AnalysisResult = analyze_ticket(message)

    ticket = Ticket(
        message=message,
        category=result.category,
        priority=result.priority,
        urgency=result.urgency,
        keywords=",".join(result.keywords),
        confidence=result.confidence,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_all_tickets(db: Session) -> list[Ticket]:
    """
    Retrieve all tickets ordered by creation date (newest first).

    Args:
        db: Active SQLAlchemy session.

    Returns:
        List of Ticket ORM instances.
    """
    return (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .all()
    )
