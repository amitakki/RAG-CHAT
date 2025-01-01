from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from src.domain.entities import Document, Embedding
from src.application.interfaces.vector_db_port import VectorDBPort
from src.application.exceptions import VectorDBException

class ChromaDBAdapter(VectorDBPort):
    """
    Adapter for ChromaDB implementing the VectorDBPort interface.
    Handles storage and retrieval of document embeddings.
    """
    def __init__(self, host: str, port: int, collection_name: str = "documents"):
        """
        Initialize ChromaDB connection and collection.
        
        Args:
            host: ChromaDB host address
            port: ChromaDB port number
            collection_name: Name of the collection to use
        """
        try:
            self.client = chromadb.HttpClient(
                Settings(
                    chroma_server_host=host,
                    chroma_server_port=port
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # Using cosine similarity
            )
        
        except Exception as e:
            raise VectorDBException(f"Error initializing ChromaDB: {str(e)}")

    async def store_embedding(self, document: Document, embedding: Embedding) -> None:
        """
        Stores a document and its embedding in ChromaDB.
        
        Args:
            document: Document entity to store
            embedding: Embedding vector for the document
        """
        try:
            self.collection.add(
                ids=[document.id],
                embeddings=[embedding.vector],
                metadatas=[{
                    **document.metadata,
                    "source": document.source,
                    "embedding_model": embedding.model
                }],
                documents=[document.content]
            )
        
        except Exception as e:
            raise VectorDBException(f"Error storing embedding: {str(e)}")

    async def search_similar(
        self,
        embedding: Embedding,
        limit: int = 3,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Searches for similar documents using the provided embedding.
        
        Args:
            embedding: Query embedding to search with
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score threshold
        
        Returns:
            List[Document]: List of similar documents
        """
        try:
            # Perform similarity search
            results = self.collection.query(
                query_embeddings=[embedding.vector],
                n_results=limit,
                include=['documents', 'metadatas', 'distances']
            )

            documents = []
            for i in range(len(results['ids'][0])):
                # Skip if below threshold
                if (score_threshold is not None and 
                    results['distances'][0][i] > score_threshold):
                    continue

                doc = Document(
                    id=results['ids'][0][i],
                    content=results['documents'][0][i],
                    source=results['metadatas'][0][i].get('source', ''),
                    metadata={
                        **results['metadatas'][0][i],
                        'similarity_score': 1 - results['distances'][0][i]
                    }
                )
                documents.append(doc)

            return documents

        except Exception as e:
            raise VectorDBException(f"Error searching similar documents: {str(e)}")

    async def delete_document(self, document_id: str) -> None:
        """
        Deletes a document and its embedding from ChromaDB.
        
        Args:
            document_id: ID of the document to delete
        """
        try:
            self.collection.delete(ids=[document_id])
        
        except Exception as e:
            raise VectorDBException(f"Error deleting document: {str(e)}")