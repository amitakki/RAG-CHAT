from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4


@dataclass
class Embedding:
    """
    Represents a vector embedding of text content.
    Includes metadata for tracking embedding properties and source information.
    """
    vector: List[float]
    model: str
    id: str = field(default_factory=lambda: str(uuid4()))
    metadata: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """Validates the embedding vector"""
        if not isinstance(self.vector, list) or \
           not all(isinstance(x, float) for x in self.vector):
            raise ValueError("Vector must be a list of float values")
