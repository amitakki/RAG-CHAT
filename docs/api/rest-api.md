# REST API Reference

## Authentication

All API endpoints require authentication using an API key header:

```
X-API-Key: your-api-key
```

## Endpoints

### Chat Completion

```http
POST /api/v1/chat/{session_id}/messages
```

Request Body:
```json
{
  "content": "What is machine learning?",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

Response:
```json
{
  "id": "msg_123",
  "content": "Machine learning is...",
  "role": "assistant",
  "type": "text",
  "timestamp": "2024-01-04T12:00:00Z"
}
```

### Document Management

```http
POST /api/v1/documents
```

Request Body:
```json
{
  "content": "Document content...",
  "source": "wiki",
  "metadata": {
    "author": "John Doe"
  }
}
```

Response:
```json
{
  "id": "doc_123",
  "status": "processed"
}
```

# docs/deployment/production-setup.md
# Production Deployment Guide

## System Requirements

- 4+ CPU cores
- 16GB+ RAM
- 50GB+ storage
- Ubuntu 20.04 or higher

## Deployment Steps

1. Set up server:
```bash
# Update system
sudo apt update
sudo apt upgrade

# Install dependencies
sudo apt install python3.9 python3.9-venv
```

2. Configure services:
```bash
# Configure MongoDB
sudo systemctl enable mongod
sudo systemctl start mongod

# Configure ChromaDB
docker-compose up -d chroma
```

3. Deploy application:
```bash
# Clone repository
git clone <repository-url>
cd rag-chatbot

# Setup virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install production dependencies
pip install -r requirements/prod.txt

# Configure environment
cp .env.example .env
nano .env

# Start application
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

# docs/guides/rag-configuration.md
# RAG Configuration Guide

## Vector Database Setup

1. Initialize ChromaDB:
```python
from chromadb import Client

client = Client()
collection = client.create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)
```

2. Configure embeddings:
```python
# Set up embedding model
embedding_model = "text-embedding-ada-002"
embedding_dimension = 1536
```

## Document Processing

1. Chunk configuration:
```python
chunk_size = 1000
chunk_overlap = 200
```

2. Metadata handling:
```python
metadata = {
    "source": document.source,
    "timestamp": datetime.utcnow().isoformat(),
    "author": document.metadata.get("author")
}
```

## Retrieval Configuration

1. Search parameters:
```python
search_params = {
    "k": 3,  # Number of similar documents
    "score_threshold": 0.7,  # Minimum similarity score
    "fetch_k": 10  # Initial fetch size
}
```

2. Context window:
```python
max_context_length = 2000  # Maximum context length in tokens
```