"""
FastAPI router for ticket-related endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.ticket import (
    TicketAnalyzeRequest,
    TicketAnalyzeResponse,
    TicketListItem,
)
from app.controllers.ticket_controller import (
    handle_analyze_ticket,
    handle_get_tickets,
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post(
    "/analyze",
    response_model=TicketAnalyzeResponse,
    status_code=201,
    summary="Analyze a support ticket",
    description="Runs the local NLP engine on the supplied message, stores "
                "the result, and returns the analysis.",
)
def analyze_ticket(
    payload: TicketAnalyzeRequest,
    db: Session = Depends(get_db),
):
    return handle_analyze_ticket(payload, db)


@router.get(
    "",
    response_model=list[TicketListItem],
    summary="List all tickets",
    description="Returns every analyzed ticket, newest first.",
)
def list_tickets(db: Session = Depends(get_db)):
    return handle_get_tickets(db)
