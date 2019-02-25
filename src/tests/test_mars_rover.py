import re

import pytest


class Position:

    def __init__(self, horizontal: int, vertical: int) -> None:
        self._horizontal = horizontal
        self._vertical = vertical

    def moved_vertically_by(self, points: int) -> 'Position':
        return Position(self._horizontal, self._vertical + points)

    def horizontal(self) -> int:
        return self._horizontal

    def vertical(self) -> int:
        return self._vertical

    def __repr__(self) -> str:  # pragma: nocover
        return f'{self.__class__.__name__}({self._horizontal!r}, {self._vertical!r})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):  # pragma: nocover
            return NotImplemented
        return self._horizontal == other._horizontal and self._vertical == other._vertical


class Rover:

    def __init__(self, position: Position) -> None:
        self._position = position

    def move_forward(self) -> None:
        self._position = self._position.moved_vertically_by(1)

    def move_backward(self) -> None:
        self._position = self._position.moved_vertically_by(-1)

    def position(self) -> Position:
        return self._position


class MarsRoverApplication:

    @classmethod
    def landing_with(cls, rover_position: str) -> 'MarsRoverApplication':
        match = re.match(r'^(\d+) (\d+)$', rover_position)
        if not match:
            raise ValueError(f'Invalid position: {rover_position}')
        return cls(Position(int(match.group(1)), int(match.group(2))))

    def __init__(self, rover_position: Position) -> None:
        self._rover = Rover(rover_position)

    def rover_position(self) -> str:
        return f'{self._rover.position().horizontal()} {self._rover.position().vertical()}'

    def execute(self, command: str) -> None:
        if command == 'f':
            self._rover.move_forward()
        elif command == 'b':
            self._rover.move_backward()
        else:
            raise RuntimeError(f'Unknown command: {command!r}')


class TestMarsRoverApplication:

    def land_rover_with_position(self, position: str) -> MarsRoverApplication:
        return MarsRoverApplication.landing_with(position)

    def test_lands_rover_with_the_given_position(self) -> None:
        app = self.land_rover_with_position('3 4')
        assert app.rover_position() == '3 4'

    @pytest.mark.parametrize('position', ['34', 'a 4', '4 a'])
    def test_rejects_invalid_initial_position(self, position: str) -> None:
        with pytest.raises(ValueError) as error:
            self.land_rover_with_position(position)
        assert str(error.value) == 'Invalid position: ' + position

    @pytest.mark.parametrize(
        ('initial_position', 'final_position'), [
            ('3 4', '3 5'),
            ('3 3', '3 4'),
            ('2 3', '2 4'),
        ]
    )
    def test_moves_rover_forward_north(
            self,
            initial_position: str,
            final_position: str,
    ) -> None:
        app = self.land_rover_with_position(initial_position)
        app.execute('f')
        assert app.rover_position() == final_position

    @pytest.mark.parametrize(
        ('initial_position', 'final_position'), [
            ('3 4', '3 3'),
            ('3 3', '3 2'),
            ('2 3', '2 2'),
        ]
    )
    def test_moves_rover_backward_from_north(
            self,
            initial_position: str,
            final_position: str,
    ) -> None:
        app = self.land_rover_with_position(initial_position)
        app.execute('b')
        assert app.rover_position() == final_position

    def test_rejects_unknown_commands(self) -> None:
        app = self.land_rover_with_position('3 4')
        with pytest.raises(RuntimeError) as error:
            app.execute('x')
        assert str(error.value) == "Unknown command: 'x'"


class TestPosition:

    def test_two_equal_positions(self) -> None:
        assert Position(3, 4) == Position(3, 4)

    def test_two_positions_with_different_horizontal_point(self) -> None:
        assert Position(3, 4) != Position(2, 4)

    def test_two_positions_with_different_vertical_point(self) -> None:
        assert Position(3, 4) != Position(3, 5)

    def test_position_moved_vertically(self) -> None:
        assert Position(3, 4).moved_vertically_by(1) == Position(3, 5)
