import re

import pytest


class Direction:

    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._symbol!r})'

    def __eq__(self, other: object) -> bool:
        return True


class Coordinates:

    def __init__(self, horizontal: int, vertical: int) -> None:
        self._horizontal = horizontal
        self._vertical = vertical

    def moved_vertically_by(self, points: int) -> 'Coordinates':
        return Coordinates(self._horizontal, self._vertical + points)

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


class Rover:

    def __init__(self, coordinates: Coordinates) -> None:
        self._coordinates = coordinates

    def move_forward(self) -> None:
        self._coordinates = self._coordinates.moved_vertically_by(1)

    def move_backward(self) -> None:
        self._coordinates = self._coordinates.moved_vertically_by(-1)

    def coordinates(self) -> Coordinates:
        return self._coordinates


class MarsRoverApplication:

    @classmethod
    def landing_with(cls, rover_position: str) -> 'MarsRoverApplication':
        match = re.match(r'^(\d+) (\d+) ([NS])$', rover_position)
        if not match:
            raise ValueError(f'Invalid position: {rover_position}')
        return cls(Coordinates(int(match.group(1)), int(match.group(2))), match.group(3))

    def __init__(self, rover_coordinates: Coordinates, rover_direction: str) -> None:
        self._rover_direction = rover_direction
        self._rover = Rover(rover_coordinates)

    def rover_position(self) -> str:
        return (
            f'{self._rover.coordinates().horizontal()} '
            f'{self._rover.coordinates().vertical()} '
            f'{self._rover_direction}'
        )

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

    @pytest.mark.parametrize(
        'position', [
            '3 4 N',
            '2 3 N',
            '3 4 S',
        ]
    )
    def test_lands_rover_at_given_coordinates_and_facing_direction(self, position: str) -> None:
        app = self.land_rover_with_position(position)
        assert app.rover_position() == position

    @pytest.mark.parametrize(
        'position', [
            '34 N',
            'a 4 N',
            '4 a N',
            '3 4 5',
            '3 4 NS',
        ]
    )
    def test_rejects_invalid_initial_position(self, position: str) -> None:
        with pytest.raises(ValueError) as error:
            self.land_rover_with_position(position)
        assert str(error.value) == 'Invalid position: ' + position

    @pytest.mark.parametrize(
        ('initial_position', 'final_position'), [
            ('3 4 N', '3 5 N'),
            ('3 3 N', '3 4 N'),
            ('2 3 N', '2 4 N'),
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
            ('3 4 N', '3 3 N'),
            ('3 3 N', '3 2 N'),
            ('2 3 N', '2 2 N'),
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
        app = self.land_rover_with_position('3 4 N')
        with pytest.raises(RuntimeError) as error:
            app.execute('x')
        assert str(error.value) == "Unknown command: 'x'"


class TestCoordinates:

    def test_two_equal_coordinates(self) -> None:
        assert Coordinates(3, 4) == Coordinates(3, 4)

    def test_two_coordinates_with_different_horizontal_point(self) -> None:
        assert Coordinates(3, 4) != Coordinates(2, 4)

    def test_two_coordinates_with_different_vertical_point(self) -> None:
        assert Coordinates(3, 4) != Coordinates(3, 5)

    def test_coordinates_moved_vertically(self) -> None:
        assert Coordinates(3, 4).moved_vertically_by(1) == Coordinates(3, 5)


class TestDirection:

    def test_two_equal_directions(self) -> None:
        assert Direction('N') == Direction('N')
