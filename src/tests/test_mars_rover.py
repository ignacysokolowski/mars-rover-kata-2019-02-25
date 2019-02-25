import re

import pytest


class Direction:

    @classmethod
    def for_symbol(cls, symbol: str) -> 'Direction':
        if symbol == 'N':
            return cls.north()
        elif symbol == 'S':
            return cls.south()
        else:
            raise ValueError(f'Unknown direction: {symbol}')

    @classmethod
    def north(cls) -> 'Direction':
        return Direction('N')

    @classmethod
    def south(cls) -> 'Direction':
        return Direction('S')

    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

    def symbol(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._symbol!r})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Direction):  # pragma: nocover
            return NotImplemented
        return self._symbol == other._symbol


class Coordinates:

    def __init__(self, horizontal: int, vertical: int) -> None:
        self._horizontal = horizontal
        self._vertical = vertical

    def moved_north(self) -> 'Coordinates':
        return self._moved_vertically_by(1)

    def moved_south(self) -> 'Coordinates':
        return self._moved_vertically_by(-1)

    def _moved_vertically_by(self, points: int) -> 'Coordinates':
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

    def __init__(self, coordinates: Coordinates, direction: Direction) -> None:
        self._coordinates = coordinates
        self._direction = direction

    def move_forward(self) -> None:
        if self._direction == Direction.north():
            self._coordinates = self._coordinates.moved_north()
        else:
            self._coordinates = self._coordinates.moved_south()

    def move_backward(self) -> None:
        if self._direction == Direction.north():
            self._coordinates = self._coordinates.moved_south()
        else:
            self._coordinates = self._coordinates.moved_north()

    def coordinates(self) -> Coordinates:
        return self._coordinates

    def direction(self) -> Direction:
        return self._direction


class UserInputError(Exception):

    @classmethod
    def invalid_position(cls, position: str) -> 'UserInputError':
        return cls(f'Invalid position: {position}')

    @classmethod
    def unknown_command(cls, command: str) -> 'UserInputError':
        return cls(f'Unknown command: {command!r}')


class MarsRoverApplication:

    @classmethod
    def landing_with(cls, rover_position: str) -> 'MarsRoverApplication':
        match = re.match(r'^(\d+) (\d+) ([A-Z])$', rover_position)
        if not match:
            raise UserInputError.invalid_position(rover_position)
        try:
            direction = Direction.for_symbol(match.group(3))
        except ValueError:
            raise UserInputError.invalid_position(rover_position)
        return cls(Coordinates(int(match.group(1)), int(match.group(2))), direction)

    def __init__(self, rover_coordinates: Coordinates, rover_direction: Direction) -> None:
        self._rover = Rover(rover_coordinates, rover_direction)

    def rover_position(self) -> str:
        return (
            f'{self._rover.coordinates().horizontal()} '
            f'{self._rover.coordinates().vertical()} '
            f'{self._rover.direction().symbol()}'
        )

    def execute(self, command: str) -> None:
        if command == 'f':
            self._rover.move_forward()
        elif command == 'b':
            self._rover.move_backward()
        else:
            raise UserInputError.unknown_command(command)


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
        ]
    )
    def test_rejects_invalid_initial_coordinates(self, position: str) -> None:
        with pytest.raises(UserInputError) as error:
            self.land_rover_with_position(position)
        assert str(error.value) == 'Invalid position: ' + position

    @pytest.mark.parametrize(
        'position', [
            '3 4 5',
            '3 4 NS',
        ]
    )
    def test_rejects_invalid_initial_direction(self, position: str) -> None:
        with pytest.raises(UserInputError) as error:
            self.land_rover_with_position(position)
        assert str(error.value) == 'Invalid position: ' + position

    @pytest.mark.parametrize(
        ('initial_position', 'final_position'), [
            ('3 4 N', '3 5 N'),
            ('3 3 N', '3 4 N'),
            ('2 3 N', '2 4 N'),
            ('3 4 S', '3 3 S'),
            ('3 3 S', '3 2 S'),
            ('2 3 S', '2 2 S'),
        ]
    )
    def test_moves_rover_forward(
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
            ('3 4 S', '3 5 S'),
            ('3 3 S', '3 4 S'),
            ('2 3 S', '2 4 S'),
        ]
    )
    def test_moves_rover_backward(
            self,
            initial_position: str,
            final_position: str,
    ) -> None:
        app = self.land_rover_with_position(initial_position)
        app.execute('b')
        assert app.rover_position() == final_position

    def test_rejects_unknown_commands(self) -> None:
        app = self.land_rover_with_position('3 4 N')
        with pytest.raises(UserInputError) as error:
            app.execute('x')
        assert str(error.value) == "Unknown command: 'x'"


class TestCoordinates:

    def test_two_equal_coordinates(self) -> None:
        assert Coordinates(3, 4) == Coordinates(3, 4)

    def test_two_coordinates_with_different_horizontal_point(self) -> None:
        assert Coordinates(3, 4) != Coordinates(2, 4)

    def test_two_coordinates_with_different_vertical_point(self) -> None:
        assert Coordinates(3, 4) != Coordinates(3, 5)


class TestDirection:

    @pytest.mark.parametrize(
        ('symbol', 'direction'), [
            ('N', Direction.north()),
            ('S', Direction.south()),
        ],
    )
    def test_can_be_created_from_symbol(self, symbol: str, direction: Direction) -> None:
        assert Direction.for_symbol(symbol) == direction

    def test_can_not_be_created_from_unknown_symbol(self) -> None:
        with pytest.raises(ValueError) as error:
            Direction.for_symbol('X')
        assert str(error.value) == 'Unknown direction: X'

    def test_two_equal_directions(self) -> None:
        assert Direction.north() == Direction.north()

    def test_two_different_directions(self) -> None:
        assert Direction.north() != Direction.south()
