from fastapi import FastAPI
from app.api.v1.endpoints import health


app = FastAPI(title="AI Knowledge Orchestrator", version="1.0.0")
app.include_router(health.router, prefix="/api/v1")
