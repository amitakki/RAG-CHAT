from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, validator


class MessageRequest(BaseModel):
    """
    Request model for sending messages. Provides input validation
    and documentation through Pydantic.
    """
    content: str = Field(
        ...,
        description="The content of the message",
        min_length=1,
        max_length=4096
    )
    temperature: Optional[float] = Field(
        0.7,
        description="Controls randomness in the response",
        ge=0.0,
        le=1.0
    )
    max_tokens: Optional[int] = Field(
        None,
        description="Maximum length of the generated response",
        gt=0,
        le=4096
    )

    @validator('content')
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()


class MessageResponse(BaseModel):
    """Response model for messages returned by the API"""
    id: str
    content: str
    role: str
    type: str
    timestamp: datetime
    metadata: Optional[Dict[str, str]] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "msg_123",
                "content": "Hello! How can I help you today?",
                "role": "assistant",
                "type": "text",
                "timestamp": "2024-03-21T14:30:00Z",
                "metadata": {"model": "gpt-4"}
            }
        }


class DocumentRequest(BaseModel):
    """Request model for document ingestion"""
    content: str = Field(..., description="The document content")
    source: str = Field(..., description="Source of the document")
    metadata: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Additional metadata for the document"
    )
    chunk_size: Optional[int] = Field(
        None,
        description="Size of chunks for document splitting",
        gt=100
    )


class ErrorResponse(BaseModel):
    """Standardized error response model"""
    error: str
    details: Optional[str] = None
    code: str

    class Config:
        schema_extra = {
            "example": {
                "error": "Invalid request",
                "details": "Message content cannot be empty",
                "code": "VALIDATION_ERROR"
            }
        }
