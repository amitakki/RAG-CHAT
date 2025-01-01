from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Message, Embedding

class LLMPort(ABC):
    """
    Port interface for Language Model operations.
    This interface abstracts the LLM provider, allowing for easy switching between different implementations.
    """
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Message:
        """
        Generates a response based on the conversation history.
        
        Args:
            messages: List of previous messages in the conversation
            temperature: Controls randomness in the response (0-1)
            max_tokens: Maximum length of the generated response
            
        Returns:
            Message: The generated response as a Message entity
        """
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> Embedding:
        """
        Generates an embedding vector for the given text.
        
        Args:
            text: The text to generate an embedding for
            
        Returns:
            Embedding: The generated embedding vector
        """
        pass