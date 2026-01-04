# app/models/db.py
"""
Database configuration and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to True to see SQL queries in logs (useful for learning!)
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()


# Dependency injection function for FastAPI routes
def get_db() -> Session:
    """
    Provides a database session for each request.
    
    Usage in FastAPI:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    
    The session is automatically closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.
    
    This should be called on application startup.
    In production, use Alembic migrations instead.
    """
    # Import models here to ensure they're registered with Base
    from app.models.document import Document
    from app.models.session import Session as SessionModel
    
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
