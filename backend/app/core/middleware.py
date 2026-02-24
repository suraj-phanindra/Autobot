import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Adds an X-Process-Time header to every response with the request duration in ms."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        response.headers["X-Process-Time"] = str(duration_ms)
        return response


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Extracts tenant context from the request and attaches it to request state.

    This middleware inspects the X-Tenant-ID header (for internal services) or
    resolves tenant from the authenticated user's JWT. The resolved tenant_id is
    placed on ``request.state.tenant_id`` for downstream use.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Allow tenant_id to be passed via header (useful for service-to-service calls)
        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            request.state.tenant_id = tenant_id
        else:
            # Will be populated later by the auth dependency if not set here
            request.state.tenant_id = None

        response = await call_next(request)
        return response
