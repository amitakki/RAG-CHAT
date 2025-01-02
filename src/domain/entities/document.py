from dataclasses import dataclass, field
from typing import List, Dict, Optional
from uuid import uuid4
from .embedding import Embedding


@dataclass
class Document:
    """
    Represents a document that can be used as context in the RAG system.
    Documents can have multiple embeddings for different models or purposes.
    """
    content: str
    source: str
    id: str = field(default_factory=lambda: str(uuid4()))
    embeddings: List[Embedding] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    chunk_size: Optional[int] = None

    def add_embedding(self, embedding: Embedding) -> None:
        """Adds a new embedding to the document"""
        self.embeddings.append(embedding)

    def get_embedding_by_model(self, model: str) -> Optional[Embedding]:
        """Retrieves an embedding for a specific model"""
        return next((emb for emb in self.embeddings
                     if emb.model == model), None)
