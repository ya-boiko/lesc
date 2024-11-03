from fastapi import FastAPI

from container import Container
from settings import Settings


def create_app():
    """Creates the application."""
    container = Container()
    container.config.from_dict(Settings().model_dump())

    return build_app()


def build_app():
    """Builds the application."""
    app = FastAPI(
        title="LESC",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    return app
