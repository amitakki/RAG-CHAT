from typing import List, Optional
from src.domain.entities import Document
from src.application.interfaces.llm_port import LLMPort
from src.application.interfaces.vector_db_port import VectorDBPort

class DocumentIngestionUseCase:
    """
    Use case for ingesting documents into the RAG system.
    Handles document processing, embedding generation, and storage.
    """
    def __init__(self, llm: LLMPort, vector_db: VectorDBPort):
        self.llm = llm
        self.vector_db = vector_db

    async def execute(
        self,
        documents: List[Document],
        chunk_size: Optional[int] = None
    ) -> None:
        """
        Processes and stores documents with their embeddings.
        Optionally chunks documents for better retrieval.
        
        Args:
            documents: List of documents to process
            chunk_size: Optional size for document chunking
        """
        for document in documents:
            # Optionally chunk the document
            if chunk_size:
                chunks = self._chunk_document(document, chunk_size)
            else:
                chunks = [document]

            # Process each chunk
            for chunk in chunks:
                # Generate embedding
                embedding = await self.llm.generate_embedding(chunk.content)
                chunk.add_embedding(embedding)

                # Store in vector database
                await self.vector_db.store_embedding(chunk, embedding)

    def _chunk_document(
        self,
        document: Document,
        chunk_size: int,
        overlap: int = 100
    ) -> List[Document]:
        """
        Splits a document into smaller chunks with overlap.
        Preserves document metadata while creating new IDs for chunks.
        """
        content = document.content
        chunks = []
        
        # Split content into overlapping chunks
        for i in range(0, len(content), chunk_size - overlap):
            chunk_content = content[i:i + chunk_size]
            if len(chunk_content) < chunk_size // 2:  # Skip small final chunks
                continue
                
            chunk = Document(
                content=chunk_content,
                source=document.source,
                metadata={
                    **document.metadata,
                    "parent_id": document.id,
                    "chunk_index": len(chunks)
                }
            )
            chunks.append(chunk)

        return chunks