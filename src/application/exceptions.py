class ApplicationException(Exception):
    """Base exception for application layer errors"""
    pass

class LLMException(ApplicationException):
    """Raised when LLM operations fail"""
    pass

class VectorDBException(ApplicationException):
    """Raised when vector database operations fail"""
    pass

class ChatRepositoryException(ApplicationException):
    """Raised when chat repository operations fail"""
    pass