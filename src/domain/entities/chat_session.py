from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from uuid import uuid4
from .message import Message


@dataclass
class ChatSession:
    """
    Represents a chat conversation session.
    Maintains the history of messages and session-specific metadata.
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    messages: List[Message] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, message: Message) -> None:
        """
        Adds a new message to the session and updates last activity timestamp.
        """
        self.messages.append(message)
        self.last_activity = datetime.utcnow()

    def get_history(self, limit: Optional[int] = None) -> List[Message]:
        """
        Retrieves chat history, optionally limited to the last n messages.
        """
        if limit is None:
            return self.messages
        return self.messages[-limit:]

    def get_context_window(self, window_size: int = 10) -> List[Message]:
        """
        Returns the most recent messages within the context window.
        Useful for maintaining context within token limits.
        """
        return self.get_history(limit=window_size)

    @property
    def message_count(self) -> int:
        """Returns the total number of messages in the session"""
        return len(self.messages)
