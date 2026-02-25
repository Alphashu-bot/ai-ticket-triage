"""
Pydantic schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------------------------

class TicketAnalyzeRequest(BaseModel):
    """Payload sent by the client for ticket analysis."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The raw support ticket message to analyze.",
        json_schema_extra={"example": "my payment failed and this is urgent"},
    )


# ---------------------------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------------------------

class TicketAnalyzeResponse(BaseModel):
    """Result returned after analyzing a single ticket."""
    id: int
    category: str
    priority: str
    urgency: bool
    keywords: list[str]
    confidence: float
    message: str

    model_config = {"from_attributes": True}


class TicketListItem(BaseModel):
    """Compact representation used in the ticket history list."""
    id: int
    message: str
    category: str
    priority: str
    urgency: bool
    keywords: list[str]
    confidence: float
    created_at: datetime

    model_config = {"from_attributes": True}
