# RAG-Enabled Chatbot with Clean Architecture

A production-ready implementation of a RAG (Retrieval Augmented Generation) chatbot using Clean Architecture principles. This project demonstrates how to build a maintainable and scalable chatbot system that can be easily extended with new features while maintaining separation of concerns.

## 🏗️ Architecture Overview

This project follows Clean Architecture principles, organizing code into concentric layers with dependencies pointing inward. Each layer has a specific responsibility and is isolated from the others through well-defined interfaces.

![RAG-Chat Architectural Diagram](https://miro.medium.com/v2/resize:fit:828/format:webp/0*CPdBD50_pGdZULyX)

### Architectural Layers

#### 1. Domain Layer (Core)
The innermost layer containing business logic and rules. It has no dependencies on outer layers or frameworks.

**Key Components:**
- `Message`: Represents chat messages
- `ChatSession`: Manages conversation state
- `Document`: Represents documents for RAG
- `Embedding`: Handles vector representations
- `MessageType`: Value object for message types

**Location:** `src/domain/`

#### 2. Application Layer
Contains application-specific business rules and orchestrates the flow of data between layers.

**Key Components:**
- `ChatCompletionUseCase`: Handles chat interaction flow
- `DocumentIngestionUseCase`: Manages document processing
- Interface ports for external services
- Application services for shared functionality

**Location:** `src/application/`

#### 3. Infrastructure Layer
Implements interfaces defined by the application layer and handles external concerns.

**Key Components:**
- `OpenAIAdapter`: Implements LLM functionality
- `ChromaDBAdapter`: Handles vector storage
- `MongoDBChatRepository`: Manages chat persistence
- Configuration management
- Dependency injection container

**Location:** `src/infrastructure/`

#### 4. Presentation Layer
Handles user interaction and API endpoints.

**Key Components:**
- Streamlit UI implementation
- FastAPI routes and handlers
- Request/Response schemas
- Input validation

**Location:** `src/presentation/`

## 🔧 Technical Stack

- **Frontend**: Streamlit
- **API Framework**: FastAPI
- **Language Model**: OpenAI GPT
- **Vector Database**: ChromaDB
- **Session Storage**: MongoDB
- **Testing**: pytest
- **Documentation**: MkDocs
- **Dependency Injection**: dependency-injector

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- MongoDB
- ChromaDB
- OpenAI API key

### Installation

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

### Running the Application

1. Initialize the database:
```bash
python -m src.main init-db
```

2. Start the application:
```bash
streamlit run src/main.py
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest
```

Generate coverage report:
```bash
pytest --cov=src --cov-report=html
```

## 📚 Project Structure

```
rag_chatbot/
│
├── src/
│   ├── domain/           # Domain entities and business rules
│   ├── application/      # Use cases and interface ports
│   ├── infrastructure/   # External implementations
│   └── presentation/     # UI and API interfaces
│
├── tests/               # Test suite
├── docs/               # Documentation
└── requirements/       # Dependency specifications
```

## 🔄 Clean Architecture Benefits

1. **Independence of Frameworks**
   - Core business logic is isolated from external frameworks
   - Easy to swap out technologies (e.g., different LLMs or databases)

2. **Testability**
   - Business rules can be tested without UI, database, or external services
   - Mocking external dependencies is straightforward

3. **Independence of UI**
   - UI can be changed without affecting business rules
   - Supports both CLI and web interfaces

4. **Independence of Database**
   - Business rules aren't bound to a specific database
   - Easy to switch between different storage solutions

5. **Independence of External Services**
   - Can swap between different LLM providers
   - Vector database implementation can be changed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 Design Decisions

### Why Clean Architecture?
- Separates concerns into layers
- Makes the system highly maintainable and testable
- Allows for easy extension and modification

### Why Streamlit?
- Rapid UI development
- Built-in state management
- Easy integration with Python backend

### Why ChromaDB?
- Open-source vector database
- Good performance for RAG applications
- Easy to set up and maintain

## 📖 Documentation

Detailed documentation is available in the `/docs` directory. To serve the documentation locally:

```bash
mkdocs serve
```

## 🛠️ Development

### Code Style
- Black for formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

### Pre-commit Hooks
Setup pre-commit hooks:
```bash
pre-commit install
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
