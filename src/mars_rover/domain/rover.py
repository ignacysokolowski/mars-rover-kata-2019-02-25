from .position import Position


class RoverOutsideSurface(Exception):
    pass


class Rover:

    def __init__(self, position: Position) -> None:
        if position.coordinates().horizontal() > 5 or position.coordinates().vertical() > 5:
            raise RoverOutsideSurface()
        self._position = position

    def move_forward(self) -> None:
        self._position = self._position.moved_forward()

    def move_backward(self) -> None:
        self._position = self._position.moved_backward()

    def turn_right(self) -> None:
        self._position = self._position.turned_right()

    def turn_left(self) -> None:
        self._position = self._position.turned_left()

    def position(self) -> Position:
        return self._position
