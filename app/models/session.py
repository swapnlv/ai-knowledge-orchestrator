# app/models/session.py
"""
Session model - stores conversation sessions for multi-turn chats
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.db import Base


class Session(Base):
    """
    Represents a conversation session.
    
    Used in Milestone 5 for conversational memory.
    For now, it's just a placeholder to complete the schema.
    
    Attributes:
        id: Primary key
        session_id: Unique session identifier (UUID)
        user_id: Optional user identifier
        created_at: When session started
        updated_at: Last activity timestamp
    """
    __tablename__ = "sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(100))
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def __repr__(self) -> str:
        return f"Session(id={self.id!r}, session_id={self.session_id!r})"
