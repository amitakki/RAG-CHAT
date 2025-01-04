import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from src.domain.entities import Message, Document, Embedding, MessageType
from src.application.interfaces.llm_port import LLMPort
from src.application.interfaces.vector_db_port import VectorDBPort
from src.application.interfaces.chat_repository_port import ChatRepositoryPort
from src.application.services.prompt_service import PromptService
from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.application.use_cases.document_ingestion import DocumentIngestionUseCase


@pytest.fixture
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def mock_llm() -> AsyncGenerator[Mock, None]:
    """Create a mock LLM port implementation."""
    mock = AsyncMock(spec=LLMPort)
    mock.generate_response.return_value = Message(
        content="Mocked response",
        role="assistant",
        type=MessageType.TEXT
    )
    mock.generate_embedding.return_value = Embedding(
        vector=[0.1, 0.2, 0.3],
        model="test-model"
    )
    yield mock


@pytest.fixture
async def mock_vector_db() -> AsyncGenerator[Mock, None]:
    """Create a mock vector database port implementation."""
    mock = AsyncMock(spec=VectorDBPort)
    mock.search_similar.return_value = [
        Document(
            content="Test document",
            source="test",
            metadata={"key": "value"}
        )
    ]
    yield mock


@pytest.fixture
async def mock_chat_repository() -> AsyncGenerator[Mock, None]:
    """Create a mock chat repository port implementation."""
    mock = AsyncMock(spec=ChatRepositoryPort)
    yield mock


@pytest.fixture
def prompt_service() -> PromptService:
    """Create a real instance of PromptService."""
    return PromptService()


@pytest.fixture
async def chat_completion_use_case(
    mock_llm: Mock,
    mock_vector_db: Mock,
    mock_chat_repository: Mock,
    prompt_service: PromptService
) -> AsyncGenerator[ChatCompletionUseCase, None]:
    """Create a ChatCompletionUseCase instance with mock dependencies."""
    use_case = ChatCompletionUseCase(
        llm=mock_llm,
        vector_db=mock_vector_db,
        chat_repository=mock_chat_repository,
        prompt_service=prompt_service
    )
    yield use_case
