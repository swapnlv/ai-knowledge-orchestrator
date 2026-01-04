# app/api/v1/endpoints/documents.py
"""
Document management endpoints
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.db import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentPublic

router = APIRouter()

# Type alias for dependency injection
SessionDep = Annotated[Session, Depends(get_db)]


@router.post("/documents", response_model=DocumentPublic, status_code=status.HTTP_201_CREATED)
def create_document(document: DocumentCreate, db: SessionDep):
    """
    Create a new document.
    
    This endpoint:
    1. Validates input using Pydantic (DocumentCreate)
    2. Creates SQLAlchemy model instance
    3. Saves to database
    4. Returns response (DocumentPublic)
    
    Example request:
        POST /v1/documents
        {
            "title": "Python Guide",
            "source_type": "pdf",
            "source_path": "/uploads/python.pdf",
            "content_preview": "Python is a programming language..."
        }
    """
    # Convert Pydantic model to SQLAlchemy model
    db_document = Document(**document.model_dump())
    
    # Save to database
    db.add(db_document)
    db.commit()
    db.refresh(db_document)  # Get the generated ID and timestamps
    
    return db_document


@router.get("/documents", response_model=list[DocumentPublic])
def list_documents(db: SessionDep, skip: int = 0, limit: int = 100):
    """
    List all documents with pagination.
    
    Query parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to return (default: 100)
    """
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents


@router.get("/documents/{document_id}", response_model=DocumentPublic)
def get_document(document_id: int, db: SessionDep):
    """
    Get a specific document by ID.
    
    Returns 404 if document doesn't exist.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )
    
    return document


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: SessionDep):
    """
    Delete a document by ID.
    
    Returns 204 No Content on success.
    Returns 404 if document doesn't exist.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )
    
    db.delete(document)
    db.commit()
    
    return None
