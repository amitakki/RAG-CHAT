from fastapi import Request
from fastapi.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging requests and responses.
    Tracks timing and basic metrics.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)

            # Log response timing
            duration = time.time() - start_time
            logger.info(
                f"Response: {response.status_code} "
                f"Duration: {duration:.3f}s"
            )

            return response

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "code": "INTERNAL_ERROR"
                }
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware for basic rate limiting.
    Uses a simple rolling window approach.
    """
    def __init__(self, app, rate_limit: int = 100):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Check rate limit
        current_time = time.time()
        if not self._check_rate_limit(client_ip, current_time):
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too many requests",
                    "code": "RATE_LIMIT_EXCEEDED"
                }
            )

        return await call_next(request)

    def _check_rate_limit(self, client_ip: str, current_time: float) -> bool:
        # Clean old requests
        window_start = current_time - 3600  # 1 hour window

        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if t > window_start
            ]

            if len(self.requests[client_ip]) >= self.rate_limit:
                return False

        self.requests.setdefault(client_ip, []).append(current_time)
        return True
