from functools import total_ordering

from .direction import Direction
from .step import Step


@total_ordering
class Coordinates:

    def __init__(self, horizontal: int, vertical: int) -> None:
        self._horizontal = horizontal
        self._vertical = vertical

    def moved_in(self, direction: Direction) -> 'Coordinates':
        return self._moved_by(direction.step())

    def _moved_by(self, step: Step) -> 'Coordinates':
        return self._moved_to(
            self._horizontal + step.points_east(),
            self._vertical + step.points_north(),
        )

    def _moved_to(self, horizontal: int, vertical: int) -> 'Coordinates':
        return Coordinates(
            horizontal if horizontal >= 0 else 0,
            vertical if vertical >= 0 else 0,
        )

    def horizontal(self) -> int:
        return self._horizontal

    def vertical(self) -> int:
        return self._vertical

    def __repr__(self) -> str:  # pragma: nocover
        return f'{self.__class__.__name__}({self._horizontal!r}, {self._vertical!r})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinates):  # pragma: nocover
            return NotImplemented
        return self._horizontal == other._horizontal and self._vertical == other._vertical

    def __gt__(self, other: 'Coordinates') -> bool:
        return self._horizontal > other._horizontal or self._vertical > other._vertical
