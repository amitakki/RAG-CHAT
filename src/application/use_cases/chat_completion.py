from typing import Optional
from src.domain.entities import Message, ChatSession
from src.domain.value_objects.message_type import MessageType
from src.application.interfaces.llm_port import LLMPort
from src.application.interfaces.vector_db_port import VectorDBPort
from src.application.interfaces.chat_repository_port import ChatRepositoryPort
from src.application.services.prompt_service import PromptService


class ChatCompletionUseCase:
    """
    Main use case for handling chat completion with RAG capabilities.
    Orchestrates the flow between different components to generate responses.
    """
    def __init__(
        self,
        llm: LLMPort,
        vector_db: VectorDBPort,
        chat_repository: ChatRepositoryPort,
        prompt_service: PromptService
    ):
        self.llm = llm
        self.vector_db = vector_db
        self.chat_repository = chat_repository
        self.prompt_service = prompt_service

    async def execute(
        self,
        session_id: str,
        user_input: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Message:
        """
        Executes the chat completion flow:
        1. Retrieves or creates chat session
        2. Generates embedding for user input
        3. Searches for relevant context
        4. Constructs prompt with context
        5. Generates response using LLM
        6. Saves the updated session
        """
        # Get or create chat session
        session = await self.chat_repository.get_session(session_id)
        if not session:
            session = ChatSession(id=session_id)

        # Create user message
        user_message = Message(
            content=user_input,
            role="user",
            type=MessageType.TEXT
        )
        session.add_message(user_message)

        # Generate embedding for user input
        input_embedding = await self.llm.generate_embedding(user_input)

        # Search for relevant context
        relevant_docs = await self.vector_db.search_similar(
            embedding=input_embedding,
            limit=3,
            score_threshold=0.7
        )

        # Construct prompt with context
        context_enhanced_prompt = \
            self.prompt_service.construct_prompt_with_context(
                user_input=user_input,
                relevant_docs=relevant_docs)

        # Generate response
        response = await self.llm.generate_response(
            messages=[
                *session.get_context_window(window_size=10),
                Message(
                    content=context_enhanced_prompt,
                    role="user",
                    type=MessageType.TEXT
                )
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Save updated session
        session.add_message(response)
        await self.chat_repository.save_session(session)

        return response
