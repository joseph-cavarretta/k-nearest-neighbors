class KNearestNeighborsError(Exception):
    """Base class for domain errors raised by this service."""


class TooManyPointsError(KNearestNeighborsError):
    """A request exceeded the configured per-list point limit."""

    def __init__(self, list_name: str, count: int, limit: int) -> None:
        self.list_name = list_name
        self.count = count
        self.limit = limit
        super().__init__(
            f"{list_name} has {count} points; the limit per list is {limit}"
        )
