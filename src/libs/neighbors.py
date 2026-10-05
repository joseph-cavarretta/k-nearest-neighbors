import numpy as np
from sklearn.neighbors import BallTree

from src.models import Coordinate, DistanceUnit, NeighborMatch, QueryResult

EARTH_RADIUS: dict[DistanceUnit, float] = {"miles": 3959.0, "kilometers": 6371.0}


def find_nearest(
    query_points: list[Coordinate],
    reference_points: list[Coordinate],
    k: int,
    unit: DistanceUnit,
    leaf_size: int,
) -> list[QueryResult]:
    """Find the k nearest reference points for each query point, nearest first.

    Builds a BallTree over the reference points with the haversine metric and
    queries it once with the query points, mirroring the notebook analysis (~850x
    faster than pairwise). k must not exceed the number of reference points.
    """
    # haversine requires radians in (lat, lon) order
    query_radians = _to_radians(query_points)
    reference_radians = _to_radians(reference_points)

    tree = BallTree(reference_radians, metric="haversine", leaf_size=leaf_size)
    distances, indices = tree.query(query_radians, k=k)
    distances = distances * EARTH_RADIUS[unit]

    return [
        QueryResult(
            query_index=query_index,
            neighbors=[
                NeighborMatch(
                    reference_index=int(reference_index),
                    coordinate=reference_points[int(reference_index)],
                    distance=float(distance),
                )
                for reference_index, distance in zip(
                    indices[query_index], distances[query_index], strict=True
                )
            ],
        )
        for query_index in range(len(query_points))
    ]


def _to_radians(points: list[Coordinate]) -> np.ndarray:
    """Convert coordinates in degrees to a (n, 2) radians array, lat first."""
    degrees = np.array([(point.lat, point.lon) for point in points])
    return np.radians(degrees)
