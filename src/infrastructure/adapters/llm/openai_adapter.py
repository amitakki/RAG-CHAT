import openai
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.domain.entities import Message, Embedding
from src.domain.value_objects.message_type import MessageType
from src.application.interfaces.llm_port import LLMPort
from src.application.exceptions import LLMException


class OpenAIAdapter(LLMPort):
    """
    Adapter for OpenAI's API implementing the LLMPort interface.
    Handles both chat completions and embeddings generation.
    """
    def __init__(self, api_key: str, model: str, embedding_model: str):
        """
        Initialize the OpenAI adapter with necessary configuration.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for chat completions
            embedding_model: Model to use for embeddings
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.embedding_model = embedding_model

    async def generate_response(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Message:
        """
        Generates a response using OpenAI's chat completion API.
        
        Args:
            messages: List of conversation messages
            temperature: Controls randomness in the response
            max_tokens: Maximum length of the generated response
        
        Returns:
            Message: The generated response as a Message entity
        """
        try:
            # Convert our domain messages to OpenAI format
            openai_messages = [
                {
                    "role": msg.role,
                    "content": msg.content
                }
                for msg in messages
            ]

            # Make API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
                stream=False
            )

            # Convert response to our domain Message
            return Message(
                content=response.choices[0].message.content,
                role="assistant",
                type=MessageType.TEXT,
                metadata={
                    "model": self.model,
                    "finish_reason": response.choices[0].finish_reason,
                }
            )

        except Exception as e:
            raise LLMException(f"Error generating response: {str(e)}")

    async def generate_embedding(self, text: str) -> Embedding:
        """
        Generates embeddings using OpenAI's embedding API.
        
        Args:
            text: Text to generate embedding for
        
        Returns:
            Embedding: The generated embedding vector
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )

            return Embedding(
                vector=response.data[0].embedding,
                model=self.embedding_model,
                metadata={
                    "text_length": len(text),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        except Exception as e:
            raise LLMException(f"Error generating embedding: {str(e)}")