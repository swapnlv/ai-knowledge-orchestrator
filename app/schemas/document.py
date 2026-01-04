# app/schemas/document.py
"""
Pydantic schemas for Document-related API operations
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class DocumentBase(BaseModel):
    """Base schema with common document fields"""
    title: str = Field(..., min_length=1, max_length=500, description="Document title")
    source_type: str = Field(..., description="Type of source: 'pdf', 'url', 'text', etc.")
    source_path: Optional[str] = Field(None, max_length=1000, description="File path or URL")
    content_preview: Optional[str] = Field(None, description="Preview of document content")


class DocumentCreate(DocumentBase):
    """
    Schema for creating a new document.
    
    Used in POST /v1/documents endpoint.
    
    Example:
        {
            "title": "Machine Learning Guide",
            "source_type": "pdf",
            "source_path": "/uploads/ml_guide.pdf",
            "content_preview": "Introduction to ML..."
        }
    """
    pass


class DocumentUpdate(BaseModel):
    """
    Schema for updating an existing document.
    
    All fields are optional - only provided fields will be updated.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    source_type: Optional[str] = None
    source_path: Optional[str] = Field(None, max_length=1000)
    content_preview: Optional[str] = None


class DocumentPublic(DocumentBase):
    """
    Schema for document responses.
    
    Includes database-generated fields like id and timestamps.
    
    Example response:
        {
            "id": 1,
            "title": "Machine Learning Guide",
            "source_type": "pdf",
            "source_path": "/uploads/ml_guide.pdf",
            "content_preview": "Introduction to ML...",
            "created_at": "2026-01-03T10:30:00Z",
            "updated_at": "2026-01-03T10:30:00Z"
        }
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    # Pydantic V2 config - allows creating from ORM models
    model_config = ConfigDict(from_attributes=True)
