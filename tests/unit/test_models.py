import pytest
from pydantic import ValidationError

from src.models import Coordinate, NeighborsRequest

VALID = Coordinate(lat=40.0, lon=-105.0)


def test_latitude_out_of_bounds_rejected() -> None:
    with pytest.raises(ValidationError):
        Coordinate(lat=91.0, lon=0.0)


def test_longitude_out_of_bounds_rejected() -> None:
    with pytest.raises(ValidationError):
        Coordinate(lat=0.0, lon=-180.5)


def test_k_greater_than_reference_count_rejected() -> None:
    with pytest.raises(ValidationError, match="exceeds reference point count"):
        NeighborsRequest(query_points=[VALID], reference_points=[VALID], k=2)


def test_empty_lists_rejected() -> None:
    with pytest.raises(ValidationError):
        NeighborsRequest(query_points=[], reference_points=[VALID])


def test_extra_fields_rejected() -> None:
    with pytest.raises(ValidationError):
        NeighborsRequest(
            query_points=[VALID],
            reference_points=[VALID],
            metric="euclidean",  # type: ignore[call-arg]  # asserting rejection
        )


def test_defaults_are_k1_miles() -> None:
    request = NeighborsRequest(query_points=[VALID], reference_points=[VALID])
    assert request.k == 1
    assert request.unit == "miles"
