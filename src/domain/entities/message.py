from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict
from uuid import uuid4
from ..value_objects.message_type import MessageType


@dataclass
class Message:
    """
    Core entity representing a message in the chat system.
    Uses dataclass for immutability and clean representation.
    """
    content: str
    role: str
    type: MessageType
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """Validates the message role after initialization"""
        valid_roles = {"user", "assistant", "system", "function"}
        if self.role not in valid_roles:
            raise ValueError(f"Invalid role: {self.role}." +
                             "Must be one of {valid_roles}")
