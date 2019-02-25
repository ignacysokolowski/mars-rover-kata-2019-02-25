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
    def landing_with(cls, position: str) -> 'MarsRoverApplication':
        return cls(position)

    def __init__(self, position: str) -> None:
        horizontal, vertical = position.split()
        self._rover = Rover(Position(int(horizontal), int(vertical)))

    def rover_position(self) -> str:
        return f'{self._rover.position().horizontal()} {self._rover.position().vertical()}'

    def execute(self, command: str) -> None:
        if command not in ('f', 'b'):
            raise RuntimeError(f'Unknown command: {command!r}')
        if command == 'f':
            self._rover.move_forward()
        else:
            self._rover.move_backward()


class TestMarsRoverApplication:

    def land_rover_with_position(self, position: str) -> MarsRoverApplication:
        return MarsRoverApplication.landing_with(position)

    def test_lands_rover_with_the_given_position(self) -> None:
        app = self.land_rover_with_position('3 4')
        assert app.rover_position() == '3 4'

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
