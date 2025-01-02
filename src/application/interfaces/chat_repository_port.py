from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import ChatSession


class ChatRepositoryPort(ABC):
    """
    Port interface for chat session persistence operations.
    Abstracts the underlying storage mechanism for chat sessions.
    """
    @abstractmethod
    async def save_session(self, session: ChatSession) -> None:
        """Saves or updates a chat session"""
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieves a chat session by ID"""
        pass

    @abstractmethod
    async def delete_session(self, session_id: str) -> None:
        """Deletes a chat session"""
        pass

    @abstractmethod
    async def list_sessions(self, limit: int = 10,
                            offset: int = 0) -> List[ChatSession]:
        """Lists chat sessions with pagination"""
        pass
