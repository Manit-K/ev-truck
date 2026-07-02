from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.project_name,
        version=settings.app_version,
        description="AI-based EV Truck Energy Optimization Platform",
    )

    app.include_router(api_router)

    return app


app = create_app()