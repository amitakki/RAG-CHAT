from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from src.infrastructure.di.container import Container
from .handlers import ChatHandler
from ..schemas.api_models import (
    MessageRequest,
    MessageResponse,
    DocumentRequest,
    ErrorResponse
)

# Create router with prefix and tags for API documentation
router = APIRouter(
    prefix="/api/v1",
    tags=["chat"],
    responses={
        500: {"model": ErrorResponse},
        503: {"model": ErrorResponse}
    }
)


@router.post(
    "/chat/{session_id}/messages",
    response_model=MessageResponse,
    summary="Send a message and get a response",
    response_description="The generated response from the assistant"
)
@inject
async def send_message(
    session_id: str,
    request: MessageRequest,
    handler: ChatHandler = Depends(Provide[Container.chat_handler])
) -> MessageResponse:
    """
    Send a message in a chat session and get a response.

    Parameters:
        session_id: Unique identifier for the chat session
        request: Message content and optional parameters

    Returns:
        MessageResponse: The generated response
    """
    return await handler.send_message(session_id, request)


@router.post(
    "/documents",
    status_code=204,
    summary="Ingest a document for RAG",
    responses={
        204: {"description": "Document successfully ingested"},
        500: {"model": ErrorResponse}
    }
)
@inject
async def ingest_document(
    request: DocumentRequest,
    handler: ChatHandler = Depends(Provide[Container.chat_handler])
) -> None:
    """
    Ingest a document for use in RAG responses.

    Parameters:
        request: Document content and metadata
    """
    await handler.ingest_documents(request)
