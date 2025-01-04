import pytest
import asyncio
import time
from src.infrastructure.di.container import Container


@pytest.mark.asyncio
async def test_chat_completion_performance():
    """Test chat completion response time."""
    container = Container()
    chat_completion = container.chat_completion()

    start_time = time.time()

    response = await chat_completion.execute(
        session_id="perf-test",
        user_input="What is Python?"
    )

    end_time = time.time()
    duration = end_time - start_time

    # Response should be under 5 seconds
    assert duration < 5.0
    assert isinstance(response.content, str)
    assert len(response.content) > 0
