import pytest
from src.infrastructure.di.container import Container
from src.domain.entities import Document


@pytest.mark.asyncio
async def test_document_ingestion_integration():
    """Integration test for document ingestion."""
    # Arrange
    container = Container()
    document_ingestion = container.document_ingestion()

    document = Document(
        content="Python is a programming language.",
        source="test-source"
    )

    # Act
    await document_ingestion.execute(
        documents=[document],
        chunk_size=1000
    )

    # Assert - Verify document is searchable
    vector_db = container.vector_db()
    chat_completion = container.chat_completion()

    response = await chat_completion.execute(
        session_id="test-integration",
        user_input="What is Python?"
    )
    assert len(response.content) > 0
