class DomainException(Exception):
    """Base exception for domain-related errors"""
    pass


class InvalidMessageError(DomainException):
    """Raised when a message fails validation"""
    pass


class InvalidEmbeddingError(DomainException):
    """Raised when an embedding is invalid"""
    pass


class InvalidDocumentError(DomainException):
    """Raised when a document fails validation"""
    pass
