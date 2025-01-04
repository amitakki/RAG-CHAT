import pytest
from httpx import AsyncClient
from src.presentation.api.app import create_app


@pytest.mark.asyncio
async def test_chat_endpoint():
    """End-to-end test for chat endpoint."""
    app = create_app()

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/chat/test-session/messages",
            json={
                "content": "What is Python?",
                "temperature": 0.7
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert data["role"] == "assistant"
