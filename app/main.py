from fastapi import FastAPI

import app.rest_api as routers
from app.adapters.orm import bind_mappers

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
        title='LESC',
        docs_url='/api/docs',
        openapi_url='/api/openapi.json',
        on_startup=[bind_mappers],
    )

    app.include_router(routers.authRouter)

    return app
