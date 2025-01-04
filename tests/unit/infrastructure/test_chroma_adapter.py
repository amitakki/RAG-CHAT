import pytest
from unittest.mock import patch, MagicMock
from src.infrastructure.adapters.vector_db.chroma_adapter import ChromaDBAdapter
from src.application.exceptions import VectorDBException


@pytest.mark.asyncio
async def test_chroma_store_embedding():
    """Test ChromaDB adapter embedding storage."""
    # Arrange
    adapter = ChromaDBAdapter(
        host="localhost",
        port=8000
    )

    mock_collection = MagicMock()

    with patch('chromadb.HttpClient') as mock_client:
        mock_client.return_value.get_or_create_collection.return_value \
            = mock_collection

        # Act
        await adapter.store_embedding(
            document=MagicMock(id="test-id", content="test content"),
            embedding=MagicMock(vector=[0.1, 0.2, 0.3])
        )

        # Assert
        mock_collection.add.assert_called_once()
