from .coordinates import Coordinates
from .direction import Direction
from .position import Position


class Rover:

    def __init__(self, position: Position) -> None:
        self._coordinates = position.coordinates()
        self._direction = position.direction()

    def move_forward(self) -> None:
        self._coordinates = self._coordinates.moved_in(self._direction)

    def move_backward(self) -> None:
        self._coordinates = self._coordinates.moved_in(self._direction.opposite())

    def turn_right(self) -> None:
        self._direction = self._direction.next_to_the_right()

    def turn_left(self) -> None:
        self._direction = self._direction.next_to_the_left()

    def coordinates(self) -> Coordinates:
        return self._coordinates

    def direction(self) -> Direction:
        return self._direction
