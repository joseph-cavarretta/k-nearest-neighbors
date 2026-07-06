import time

from fastapi import APIRouter, Request

from src.config.settings import Settings
from src.libs.errors import TooManyPointsError
from src.libs.neighbors import find_nearest
from src.models import (
    Coordinate,
    HealthResponse,
    NeighborsRequest,
    NeighborsResponse,
)

router = APIRouter()

_READINESS_QUERY = [Coordinate(lat=40.014986, lon=-105.270546)]
_READINESS_REFERENCE = [Coordinate(lat=39.739236, lon=-104.984862)]


@router.post("/v1/neighbors")
def neighbors(request: Request, body: NeighborsRequest) -> NeighborsResponse:
    """Return the k nearest reference points for each query point."""
    settings: Settings = request.app.state.settings
    _enforce_point_limits(body, settings.max_points_per_list)

    start = time.perf_counter()
    results = find_nearest(
        query_points=body.query_points,
        reference_points=body.reference_points,
        k=body.k,
        unit=body.unit,
        leaf_size=settings.balltree_leaf_size,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000

    return NeighborsResponse(
        results=results,
        query_count=len(body.query_points),
        reference_count=len(body.reference_points),
        k=body.k,
        unit=body.unit,
        elapsed_ms=elapsed_ms,
    )


@router.get("/healthz")
def liveness() -> HealthResponse:
    """Liveness probe: the process is up and serving."""
    return HealthResponse(status="ok")


@router.get("/readyz")
def readiness(request: Request) -> HealthResponse:
    """Readiness probe: exercise the BallTree path end to end."""
    settings: Settings = request.app.state.settings
    find_nearest(
        query_points=_READINESS_QUERY,
        reference_points=_READINESS_REFERENCE,
        k=1,
        unit="miles",
        leaf_size=settings.balltree_leaf_size,
    )
    return HealthResponse(status="ok")


def _enforce_point_limits(body: NeighborsRequest, limit: int) -> None:
    """Raise TooManyPointsError if either list exceeds the configured limit."""
    if len(body.query_points) > limit:
        raise TooManyPointsError("query_points", len(body.query_points), limit)
    if len(body.reference_points) > limit:
        raise TooManyPointsError("reference_points", len(body.reference_points), limit)
