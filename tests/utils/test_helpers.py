import pytest
from typing import List
from src.domain.entities import Message, MessageType


def create_test_message(content: str, role: str = "user") -> Message:
    """Helper function to create test messages."""
    return Message(
        content=content,
        role=role,
        type=MessageType.TEXT
    )


def create_test_messages(count: int) -> List[Message]:
    """Helper function to create multiple test messages."""
    return [
        create_test_message(f"Test message {i}")
        for i in range(count)
    ]
