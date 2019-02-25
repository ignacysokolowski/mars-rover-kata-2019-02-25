from typing import Container

from .coordinates import Coordinates
from .position import Position


class RoverOutsideSurface(Exception):
    pass


class Surface(Container[Coordinates]):

    @classmethod
    def of_size(cls, size: int) -> 'Surface':
        return cls(size)

    def __init__(self, size: int) -> None:
        self._north_east = Coordinates(size, size)
        self._south_west = Coordinates(0, 0)

    def __contains__(self, coordinates: object) -> bool:
        if not isinstance(coordinates, Coordinates):  # pragma: nocover
            raise TypeError(coordinates)
        return not (coordinates > self._north_east or coordinates < self._south_west)


class Rover:

    def __init__(self, position: Position) -> None:
        self._surface = Surface.of_size(5)
        if self._outside_the_surface(position):
            raise RoverOutsideSurface()
        self._position = position

    def _outside_the_surface(self, position: Position) -> bool:
        return position.coordinates() not in self._surface

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
