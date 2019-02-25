from .coordinates import Coordinates
from .position import Position


class RoverOutsideSurface(Exception):
    pass


class Rover:

    def __init__(self, position: Position) -> None:
        if self._outside_the_surface(position):
            raise RoverOutsideSurface()
        self._position = position

    def _outside_the_surface(self, position: Position) -> bool:
        return position.coordinates() > Coordinates(5, 5)

    def move_forward(self) -> None:
        self._move_to(self._position.moved_forward())

    def move_backward(self) -> None:
        self._move_to(self._position.moved_backward())

    def _move_to(self, new_position: Position) -> None:
        if self._outside_the_surface(new_position):
            return
        self._position = new_position

    def turn_right(self) -> None:
        self._position = self._position.turned_right()

    def turn_left(self) -> None:
        self._position = self._position.turned_left()

    def position(self) -> Position:
        return self._position
