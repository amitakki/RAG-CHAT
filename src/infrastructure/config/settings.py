from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration using Pydantic.
    Loads configuration from environment variables with fallbacks.
    """
    # OpenAI Configuration
    # Required
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    # Optional with default
    openai_model: str = Field('gpt-4', env='OPENAI_MODEL')
    openai_embedding_model: str = Field('text-embedding-ada-002',
                                        env='OPENAI_EMBEDDING_MODEL')

    # ChromaDB Configuration
    chroma_host: str = Field('localhost', env='CHROMA_HOST')
    chroma_port: int = Field(8000, env='CHROMA_PORT')

    # MongoDB Configuration
    mongodb_uri: str = Field('mongodb://localhost:27017', env='MONGODB_URI')
    mongodb_db_name: str = Field('rag_chatbot', env='MONGODB_DB_NAME')

    # Additional Fields
    log_level: str = Field('INFO', env='LOG_LEVEL')
    rate_limit: int = Field(100, env='RATE_LIMIT')
    allowed_origins: List[str] = Field(['http://localhost:3000',
                                        'http://localhost:8000'],
                                       env='ALLOWED_ORIGINS')

    class Config:
        env_file = '.env'
        case_sensitive = False
