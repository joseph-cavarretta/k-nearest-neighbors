import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.app.routes import router
from src.config.settings import Settings, get_settings
from src.libs.errors import TooManyPointsError


def create_app(settings: Settings) -> FastAPI:
    """Build the FastAPI application with the given settings."""
    logging.basicConfig(level=settings.log_level)

    application = FastAPI(
        title="k-nearest-neighbors",
        description=(
            "Nearest-neighbor lookups between two coordinate lists using a "
            "haversine BallTree"
        ),
        version="0.1.0",
    )
    application.state.settings = settings
    application.include_router(router)
    application.add_exception_handler(TooManyPointsError, _too_many_points_handler)
    return application


def _too_many_points_handler(request: Request, exc: Exception) -> JSONResponse:
    """Map TooManyPointsError to HTTP 413."""
    return JSONResponse(status_code=413, content={"detail": str(exc)})


app = create_app(get_settings())
