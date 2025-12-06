# app/api/v1/endpoints/health.py

from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.ENV,
    }
