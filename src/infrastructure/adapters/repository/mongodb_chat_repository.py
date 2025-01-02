from typing import Optional, List
from datetime import datetime
import motor.motor_asyncio
from bson import ObjectId

from src.domain.entities import ChatSession, Message
from src.domain.value_objects.message_type import MessageType
from src.application.interfaces.chat_repository_port import ChatRepositoryPort
from src.application.exceptions import ChatRepositoryException


class MongoDBChatRepository(ChatRepositoryPort):
    """
    MongoDB implementation of the ChatRepositoryPort.
    Uses Motor for async MongoDB operations.
    """
    def __init__(self, uri: str, database: str):
        """
        Initialize MongoDB connection.

        Args:
            uri: MongoDB connection URI
            database: Database name to use
        """
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self.db = self.client[database]
            self.sessions = self.db.chat_sessions

        except Exception as e:
            raise ChatRepositoryException(
                f"Error connecting to MongoDB: {str(e)}")

    async def save_session(self, session: ChatSession) -> None:
        """
        Saves or updates a chat session in MongoDB.

        Args:
            session: ChatSession entity to save
        """
        try:
            # Convert session to dictionary
            session_dict = {
                "messages": [self._message_to_dict(msg)
                             for msg in session.messages],
                "metadata": session.metadata,
                "created_at": session.created_at,
                "last_activity": datetime.utcnow()
            }

            # Update or insert session
            await self.sessions.update_one(
                {"_id": ObjectId(session.id)},
                {"$set": session_dict},
                upsert=True
            )

        except Exception as e:
            raise ChatRepositoryException(f"Error saving session: {str(e)}")

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Retrieves a chat session by ID.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            Optional[ChatSession]: The retrieved session or None if not found
        """
        try:
            session_dict = await self.sessions.find_one(
                {"_id": ObjectId(session_id)}
            )

            if not session_dict:
                return None

            return self._dict_to_session(session_dict)

        except Exception as e:
            raise ChatRepositoryException(
                f"Error retrieving session: {str(e)}")

    async def delete_session(self, session_id: str) -> None:
        """
        Deletes a chat session.

        Args:
            session_id: ID of the session to delete
        """
        try:
            await self.sessions.delete_one({"_id": ObjectId(session_id)})

        except Exception as e:
            raise ChatRepositoryException(f"Error deleting session: {str(e)}")

    async def list_sessions(
        self,
        limit: int = 10,
        offset: int = 0
    ) -> List[ChatSession]:
        """
        Lists chat sessions with pagination.

        Args:
            limit: Maximum number of sessions to return
            offset: Number of sessions to skip

        Returns:
            List[ChatSession]: List of chat sessions
        """
        try:
            cursor = self.sessions.find()
            cursor.skip(offset).limit(limit)
            sessions = []

            async for session_dict in cursor:
                sessions.append(self._dict_to_session(session_dict))

            return sessions

        except Exception as e:
            raise ChatRepositoryException(f"Error listing sessions: {str(e)}")

    def _message_to_dict(self, message: Message) -> dict:
        """Helper method to convert Message entity to dictionary"""
        return {
            "id": message.id,
            "content": message.content,
            "role": message.role,
            "type": message.type.value,
            "timestamp": message.timestamp,
            "metadata": message.metadata
        }

    def _dict_to_message(self, message_dict: dict) -> Message:
        """Helper method to convert dictionary to Message entity"""
        return Message(
            id=str(message_dict["id"]),
            content=message_dict["content"],
            role=message_dict["role"],
            type=MessageType(message_dict["type"]),
            timestamp=message_dict["timestamp"],
            metadata=message_dict["metadata"]
        )

    def _dict_to_session(self, session_dict: dict) -> ChatSession:
        """Helper method to convert dictionary to ChatSession entity"""
        return ChatSession(
            id=str(session_dict["_id"]),
            messages=[
                self._dict_to_message(msg)
                for msg in session_dict["messages"]
            ],
            metadata=session_dict["metadata"],
            created_at=session_dict["created_at"],
            last_activity=session_dict["last_activity"]
        )
