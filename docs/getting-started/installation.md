# Installation Guide

## Prerequisites

Before installing the RAG Chatbot, ensure you have:

- Python 3.9 or higher
- MongoDB
- ChromaDB
- OpenAI API key

## Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements/dev.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

Configure the following services:

1. OpenAI API:
   - Set OPENAI_API_KEY in .env
   - Configure model settings

2. ChromaDB:
   - Set up ChromaDB instance
   - Configure connection settings

3. MongoDB:
   - Set up MongoDB instance
   - Configure connection URI