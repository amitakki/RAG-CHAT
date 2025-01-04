import pytest
from src.infrastructure.di.container import Container
from src.domain.entities import Message, Document


@pytest.mark.asyncio
async def test_chat_completion_integration():
    """Integration test for the chat completion flow."""
    # Arrange
    container = Container()
    chat_completion = container.chat_completion()

    # Act
    response = await chat_completion.execute(
        session_id="test-integration",
        user_input="What is Python?"
    )

    # Assert
    assert isinstance(response, Message)
    assert response.role == "assistant"
    assert len(response.content) > 0
