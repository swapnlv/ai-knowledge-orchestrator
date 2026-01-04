# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import health as health_endpoint

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
    )

    # API v1 router
    app.include_router(
        health_endpoint.router,
        prefix=settings.API_V1_PREFIX,
    )

    @app.get("/", tags=["root"])
    def read_root():
        return {"message": "AI Knowledge Orchestrator API is running"}

    return app

app = create_app()
