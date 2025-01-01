from enum import Enum

class MessageType(Enum):
    """
    Value object representing different types of messages in the system.
    Using an Enum ensures type safety and prevents invalid message types.
    """
    TEXT = "text"
    EMBEDDING = "embedding"
    SYSTEM = "system"
    FUNCTION = "function"