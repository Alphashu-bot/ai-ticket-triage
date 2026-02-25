"""
FastAPI application entry point.

Bootstraps the app, applies CORS middleware, registers routers,
and initializes the database on startup.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.db.database import init_db
from app.routes.ticket_routes import router as ticket_router


# ---------------------------------------------------------------------------
# Lifespan: run DB init once on startup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables before the first request."""
    init_db()
    yield


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Support Ticket Triage — local rule-based NLP analysis",
    lifespan=lifespan,
)

# CORS — allow the React frontend to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(ticket_router)


# ---------------------------------------------------------------------------
# Health-check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    """Simple health-check endpoint used by Docker / load balancers."""
    return {"status": "healthy", "version": settings.APP_VERSION}
