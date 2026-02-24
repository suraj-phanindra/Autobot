from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.config import get_settings
from app.core.middleware import RequestTimingMiddleware, TenantContextMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup: initialize resources (DB pool, Redis connections, etc.)
    yield
    # Shutdown: clean up resources


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    # Middleware (order matters - outermost first)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestTimingMiddleware)
    app.add_middleware(TenantContextMiddleware)

    # Routes
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


app = create_app()
