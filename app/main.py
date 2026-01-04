# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1.endpoints import health as health_endpoint
from app.api.v1.endpoints import documents as documents_endpoint
from app.models.db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager - runs on app startup and shutdown.
    
    Startup: Create database tables
    Shutdown: Cleanup (if needed)
    """
    # Startup
    print("🚀 Starting AI Knowledge Orchestrator...")
    create_tables()
    yield
    # Shutdown
    print("👋 Shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        lifespan=lifespan,  # Add lifespan handler
    )

    # API v1 routers
    app.include_router(
        health_endpoint.router,
        prefix=settings.API_V1_PREFIX,
    )
    app.include_router(
        documents_endpoint.router,
        prefix=settings.API_V1_PREFIX,
        tags=["documents"],
    )

    @app.get("/", tags=["root"])
    def read_root():
        return {"message": "AI Knowledge Orchestrator API is running"}

    return app

app = create_app()
