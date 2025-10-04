import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Format process time in human-readable format
        if process_time >= 1:
            # Show in seconds if >= 1 second
            formatted_time = f"{process_time:.3f}s"
        else:
            # Show in milliseconds if < 1 second
            formatted_time = f"{process_time * 1000:.2f}ms"

        response.headers["X-Process-Time"] = formatted_time
        return response
