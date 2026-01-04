# app/models/document.py
"""
Document model - stores metadata about ingested documents
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.models.db import Base


class Document(Base):
    """
    Represents a document in the knowledge base.
    
    Attributes:
        id: Primary key
        title: Document title
        source_type: Type of source (pdf, url, text, etc.)
        source_path: Path or URL to original document
        content_preview: First 500 chars of content (for display)
        created_at: Timestamp when document was added
        updated_at: Timestamp of last update
        metadata_: Additional JSON metadata (author, tags, etc.)
    """
    __tablename__ = "documents"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Document metadata
    title: Mapped[str] = mapped_column(String(500))
    source_type: Mapped[str] = mapped_column(String(50))  # 'pdf', 'url', 'text', etc.
    source_path: Mapped[Optional[str]] = mapped_column(String(1000))  # File path or URL
    
    # Content preview (not the full text - that goes to vector store)
    content_preview: Mapped[Optional[str]] = mapped_column(Text)  # First 500 chars
    
    # Timestamps (auto-managed)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    # Optional: store additional metadata as JSON
    # metadata_: Mapped[Optional[dict]] = mapped_column(JSON, default=dict)
    
    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}, source_type={self.source_type!r})"
