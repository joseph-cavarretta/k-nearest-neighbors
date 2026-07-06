from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

DistanceUnit = Literal["miles", "kilometers"]


class Coordinate(BaseModel):
    """A geographic point in decimal degrees."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class NeighborsRequest(BaseModel):
    """Two coordinate lists: find the k nearest reference points per query point."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    query_points: list[Coordinate] = Field(min_length=1)
    reference_points: list[Coordinate] = Field(min_length=1)
    k: int = Field(default=1, ge=1)
    unit: DistanceUnit = "miles"

    @model_validator(mode="after")
    def k_within_reference_count(self) -> Self:
        """Reject k larger than the number of reference points."""
        if self.k > len(self.reference_points):
            raise ValueError(
                f"k={self.k} exceeds reference point count "
                f"({len(self.reference_points)})"
            )
        return self


class NeighborMatch(BaseModel):
    """A single matched reference point and its distance from the query point."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    reference_index: int
    coordinate: Coordinate
    distance: float


class QueryResult(BaseModel):
    """Nearest reference matches for one query point, nearest first."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    query_index: int
    neighbors: list[NeighborMatch]


class NeighborsResponse(BaseModel):
    """Full result set for a neighbors request, with timing metadata."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    results: list[QueryResult]
    query_count: int
    reference_count: int
    k: int
    unit: DistanceUnit
    elapsed_ms: float


class HealthResponse(BaseModel):
    """Probe response body."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    status: Literal["ok"]
