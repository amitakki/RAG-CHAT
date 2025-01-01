from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Document, Embedding

class VectorDBPort(ABC):
    """
    Port interface for vector database operations.
    Abstracts the underlying vector database implementation.
    """
    @abstractmethod
    async def store_embedding(self, document: Document, embedding: Embedding) -> None:
        """Stores a document and its embedding in the vector database"""
        pass

    @abstractmethod
    async def search_similar(
        self,
        embedding: Embedding,
        limit: int = 3,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Searches for similar documents based on embedding similarity.
        
        Args:
            embedding: Query embedding to search with
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score threshold
        """
        pass

    @abstractmethod
    async def delete_document(self, document_id: str) -> None:
        """Deletes a document and its embeddings from the database"""
        pass