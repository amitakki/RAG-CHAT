import pytest
from datetime import datetime
from src.domain.entities import Message, MessageType
from src.domain.entities.exceptions import InvalidMessageError


def test_message_creation():
    """Test creating a valid message."""
    message = Message(
        content="Test message",
        role="user",
        type=MessageType.TEXT
    )

    assert message.content == "Test message"
    assert message.role == "user"
    assert message.type == MessageType.TEXT
    assert isinstance(message.timestamp, datetime)


def test_invalid_message_role():
    """Test that creating a message with invalid role raises error."""
    with pytest.raises(InvalidMessageError):
        Message(
            content="Test message",
            role="invalid_role",
            type=MessageType.TEXT
        )
