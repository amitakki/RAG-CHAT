# Architectural Overview

This project implements Clean Architecture principles to create a maintainable and scalable chatbot system. The architecture is divided into concentric layers, each with specific responsibilities and dependencies.

## Layer Structure

### Domain Layer (Core)
The innermost layer containing business logic and rules.

Key Components:
- Entities (Message, ChatSession, Document)
- Value Objects (MessageType)
- Domain Services
- Business Rules

### Application Layer
Contains application-specific business rules.

Key Components:
- Use Cases
- Interface Ports
- Application Services
- Data Transfer Objects

### Infrastructure Layer
Implements interfaces defined by inner layers.

Key Components:
- Database Adapters
- External Service Adapters
- Framework Integration
- Configuration

### Presentation Layer
Handles user interaction and API endpoints.

Key Components:
- Controllers
- Views
- Presenters
- UI Components

## Dependency Rule

The fundamental rule is that dependencies can only point inward. This means:

1. Domain Layer has no dependencies
2. Application Layer depends only on Domain Layer
3. Infrastructure Layer depends on Application and Domain Layers
4. Presentation Layer depends on all inner layers