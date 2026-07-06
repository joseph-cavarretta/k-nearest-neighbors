import pytest

from src.libs.neighbors import EARTH_RADIUS, find_nearest
from src.models import Coordinate

BOULDER = Coordinate(lat=40.014986, lon=-105.270546)
DENVER = Coordinate(lat=39.739236, lon=-104.984862)
SAN_FRANCISCO = Coordinate(lat=37.7749, lon=-122.4194)


def test_nearest_of_two_references_is_the_closer_city() -> None:
    results = find_nearest(
        query_points=[BOULDER],
        reference_points=[SAN_FRANCISCO, DENVER],
        k=1,
        unit="miles",
        leaf_size=40,
    )
    match = results[0].neighbors[0]
    assert match.reference_index == 1
    assert match.coordinate == DENVER
    assert match.distance == pytest.approx(24.3, abs=0.5)


def test_k2_returns_neighbors_nearest_first() -> None:
    results = find_nearest(
        query_points=[BOULDER],
        reference_points=[SAN_FRANCISCO, DENVER],
        k=2,
        unit="miles",
        leaf_size=40,
    )
    neighbors = results[0].neighbors
    assert len(neighbors) == 2
    assert neighbors[0].distance < neighbors[1].distance
    assert [n.reference_index for n in neighbors] == [1, 0]


def test_unit_conversion_matches_earth_radius_ratio() -> None:
    miles = find_nearest([BOULDER], [DENVER], k=1, unit="miles", leaf_size=40)
    km = find_nearest([BOULDER], [DENVER], k=1, unit="kilometers", leaf_size=40)
    ratio = km[0].neighbors[0].distance / miles[0].neighbors[0].distance
    assert ratio == pytest.approx(EARTH_RADIUS["kilometers"] / EARTH_RADIUS["miles"])


def test_one_result_per_query_point() -> None:
    results = find_nearest(
        query_points=[BOULDER, SAN_FRANCISCO],
        reference_points=[DENVER],
        k=1,
        unit="miles",
        leaf_size=40,
    )
    assert [r.query_index for r in results] == [0, 1]


def test_identical_points_have_zero_distance() -> None:
    results = find_nearest([DENVER], [DENVER], k=1, unit="miles", leaf_size=40)
    assert results[0].neighbors[0].distance == pytest.approx(0.0, abs=1e-9)
