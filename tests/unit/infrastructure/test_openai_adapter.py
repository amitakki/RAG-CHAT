import pytest
from unittest.mock import patch, AsyncMock
from src.infrastructure.adapters.llm.openai_adapter import OpenAIAdapter
from src.application.exceptions import LLMException


@pytest.mark.asyncio
async def test_openai_generate_response():
    """Test OpenAI adapter response generation."""
    # Arrange
    adapter = OpenAIAdapter(
        api_key="test-key",
        model="gpt-4",
        embedding_model="text-embedding-ada-002"
    )

    mock_response = AsyncMock()
    mock_response.choices = [
        AsyncMock(
            message=AsyncMock(content="Test response")
        )
    ]

    # Act
    with patch('openai.OpenAI') as mock_openai:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        response = await adapter.generate_response(
            messages=[],
            temperature=0.7
        )

    # Assert
    assert response.content == "Test response"
    assert response.role == "assistant"
