# RAG Chatbot Documentation

Welcome to the documentation for the RAG-enabled Chatbot project. This documentation provides comprehensive information about the system's architecture, setup, and usage.

## Overview

The RAG Chatbot is built using Clean Architecture principles, providing a maintainable and scalable solution for implementing a chatbot with Retrieval Augmented Generation capabilities.

### Key Features

- Clean Architecture implementation
- RAG-enabled responses
- Document management
- Scalable design
- Comprehensive testing
- Production-ready deployment

### Quick Links

- [Installation Guide](getting-started/installation.md)
- [API Reference](api/rest-api.md)
- [Architecture Overview](architecture/overview.md)
- [Contributing Guide](development/contributing.md)

## Project Structure

```plaintext
rag_chatbot/
├── src/
│   ├── domain/         # Core business logic
│   ├── application/    # Use cases and interfaces
│   ├── infrastructure/ # External implementations
│   └── presentation/   # UI and API layers
├── tests/             # Test suite
└── docs/              # Documentation