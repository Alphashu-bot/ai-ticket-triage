"""
Controller layer for ticket endpoints.

Controllers handle HTTP-level concerns: request parsing, response formatting,
and status codes.  Business logic is delegated to the service layer.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.ticket import (
    TicketAnalyzeRequest,
    TicketAnalyzeResponse,
    TicketListItem,
)
from app.services.ticket_service import analyze_and_store_ticket, get_all_tickets


def handle_analyze_ticket(
    payload: TicketAnalyzeRequest,
    db: Session,
) -> TicketAnalyzeResponse:
    """
    Validate input, delegate analysis + persistence, and return the result.
    """
    try:
        ticket = analyze_and_store_ticket(payload.message, db)
        return TicketAnalyzeResponse(
            id=ticket.id,
            category=ticket.category,
            priority=ticket.priority,
            urgency=ticket.urgency,
            keywords=ticket.keywords.split(",") if ticket.keywords else [],
            confidence=ticket.confidence,
            message=ticket.message,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze ticket: {str(exc)}",
        ) from exc


def handle_get_tickets(db: Session) -> list[TicketListItem]:
    """
    Return all stored tickets formatted for the frontend history table.
    """
    tickets = get_all_tickets(db)
    return [
        TicketListItem(
            id=t.id,
            message=t.message,
            category=t.category,
            priority=t.priority,
            urgency=t.urgency,
            keywords=t.keywords.split(",") if t.keywords else [],
            confidence=t.confidence,
            created_at=t.created_at,
        )
        for t in tickets
    ]
