from typing import Container

from .coordinates import Coordinates


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
