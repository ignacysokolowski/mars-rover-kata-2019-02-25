from .coordinates import Coordinates
from .direction import Direction


class Position:

    def __init__(self, direction: Direction, coordinates: Coordinates) -> None:
        self._direction = direction
        self._coordinates = coordinates

    def moved_forward(self) -> 'Position':
        return Position(self._direction, self._coordinates.moved_in(self._direction))

    def moved_backward(self) -> 'Position':
        return Position(self._direction, self._coordinates.moved_in(self._direction.opposite()))

    def turned_right(self) -> 'Position':
        return Position(self._direction.next_to_the_right(), self._coordinates)

    def turned_left(self) -> 'Position':
        return Position(self._direction.next_to_the_left(), self._coordinates)

    def direction(self) -> Direction:
        return self._direction

    def coordinates(self) -> Coordinates:
        return self._coordinates

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):  # pragma: nocover
            return NotImplemented
        return self._direction == other._direction and self._coordinates == other._coordinates
