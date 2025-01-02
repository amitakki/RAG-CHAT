from dependency_injector import containers, providers
from src.infrastructure.config.settings import Settings
from src.infrastructure.adapters.llm.openai_adapter import OpenAIAdapter
from src.infrastructure.adapters.vector_db.chroma_adapter import ChromaDBAdapter
from src.infrastructure.adapters.repository.mongodb_chat_repository import MongoDBChatRepository
from src.application.services.prompt_service import PromptService
from src.application.use_cases.chat_completion import ChatCompletionUseCase
from src.application.use_cases.document_ingestion import DocumentIngestionUseCase


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection container using dependency-injector.
    Manages the creation and lifecycle of all application components.
    """

    # Configuration
    config = providers.Singleton(Settings)

    # Services
    prompt_service = providers.Singleton(PromptService)

    # Adapters
    llm = providers.Singleton(
        OpenAIAdapter,
        api_key=config.provided.openai_api_key,
        model=config.provided.openai_model,
        embedding_model=config.provided.openai_embedding_model
    )

    vector_db = providers.Singleton(
        ChromaDBAdapter,
        host=config.provided.chroma_host,
        port=config.provided.chroma_port
    )

    chat_repository = providers.Singleton(
        MongoDBChatRepository,
        uri=config.provided.mongodb_uri,
        database=config.provided.mongodb_db_name
    )

    # Use Cases
    chat_completion = providers.Singleton(
        ChatCompletionUseCase,
        llm=llm,
        vector_db=vector_db,
        chat_repository=chat_repository,
        prompt_service=prompt_service
    )

    document_ingestion = providers.Singleton(
        DocumentIngestionUseCase,
        llm=llm,
        vector_db=vector_db
    )
