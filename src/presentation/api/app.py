from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .middleware import LoggingMiddleware, RateLimitMiddleware
from src.infrastructure.di.container import Container


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    Sets up middleware, routes, and dependency injection.
    """
    # Create FastAPI app
    app = FastAPI(
        title="RAG Chatbot API",
        description="API for chat completion with RAG capabilities",
        version="1.0.0"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Add custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, rate_limit=100)

    # Set up dependency injection
    container = Container()
    app.container = container

    # Include routers
    app.include_router(router)

    return app
