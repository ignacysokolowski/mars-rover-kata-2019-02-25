from .coordinates import Coordinates
from .direction import Direction


class Position:

    def __init__(self, direction: Direction, coordinates: Coordinates) -> None:
        self._direction = direction
        self._coordinates = coordinates

    def direction(self) -> Direction:
        return self._direction

    def coordinates(self) -> Coordinates:
        return self._coordinates

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):  # pragma: nocover
            return NotImplemented
        return self._direction == other._direction and self._coordinates == other._coordinates
