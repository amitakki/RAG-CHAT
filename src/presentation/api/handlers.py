from fastapi import HTTPException
from src.domain.entities import Document
from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.application.use_cases.document_ingestion import DocumentIngestionUseCase
from src.application.exceptions import (
    LLMException,
    VectorDBException
)

class ChatHandler:
    """
    Handles chat-related API endpoints.
    Separates business logic from route definitions.
    """
    def __init__(
        self,
        chat_completion: ChatCompletionUseCase,
        document_ingestion: DocumentIngestionUseCase
    ):
        self.chat_completion = chat_completion
        self.document_ingestion = document_ingestion

    async def send_message(
        self,
        session_id: str,
        request: MessageRequest
    ) -> MessageResponse:
        """
        Handles message sending and response generation.
        
        Args:
            session_id: ID of the chat session
            request: Validated message request
            
        Returns:
            MessageResponse: The generated response
            
        Raises:
            HTTPException: If an error occurs during processing
        """
        try:
            response = await self.chat_completion.execute(
                session_id=session_id,
                user_input=request.content,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return MessageResponse(
                id=response.id,
                content=response.content,
                role=response.role,
                type=response.type.value,
                timestamp=response.timestamp,
                metadata=response.metadata
            )

        except LLMException as e:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "Language model service unavailable",
                    "details": str(e),
                    "code": "LLM_ERROR"
                }
            )
        except VectorDBException as e:
            # Log the error but continue with standard completion
            logger.warning(f"Vector DB error: {str(e)}")
            response = await self.chat_completion.execute(
                session_id=session_id,
                user_input=request.content,
                skip_rag=True  # Fall back to non-RAG completion
            )
            return MessageResponse.from_entity(response)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Internal server error",
                    "details": str(e),
                    "code": "INTERNAL_ERROR"
                }
            )

    async def ingest_documents(
        self,
        request: DocumentRequest
    ) -> None:
        """
        Handles document ingestion for RAG.
        
        Args:
            request: Validated document request
            
        Raises:
            HTTPException: If an error occurs during ingestion
        """
        try:
            document = Document(
                content=request.content,
                source=request.source,
                metadata=request.metadata
            )
            
            await self.document_ingestion.execute(
                documents=[document],
                chunk_size=request.chunk_size
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Document ingestion failed",
                    "details": str(e),
                    "code": "INGESTION_ERROR"
                }
            )