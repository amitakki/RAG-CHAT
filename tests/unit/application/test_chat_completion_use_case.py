import pytest
from unittest.mock import AsyncMock, Mock
from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.domain.entities import Message, MessageType


@pytest.mark.asyncio
async def test_chat_completion_execution(
    chat_completion_use_case: ChatCompletionUseCase,
    mock_llm: AsyncMock,
    mock_vector_db: AsyncMock,
    mock_chat_repository: AsyncMock
):
    """Test the chat completion flow."""
    # Arrange
    session_id = "test-session"
    user_input = "What is machine learning?"

    # Act
    response = await chat_completion_use_case.execute(
        session_id=session_id,
        user_input=user_input
    )

    # Assert
    assert isinstance(response, Message)
    assert response.role == "assistant"
    mock_llm.generate_embedding.assert_called_once()
    mock_vector_db.search_similar.assert_called_once()
    mock_chat_repository.save_session.assert_called_once()
