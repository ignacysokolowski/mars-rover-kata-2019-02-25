from typing import Optional

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


class MarsRoverApplication:

    def __init__(self) -> None:
        self._rover_position: Optional[Position] = None

    def rover_position(self) -> Optional[str]:
        if not self._rover_position:
            return None
        return f'{self._rover_position.horizontal()} {self._rover_position.vertical()}'

    def land_rover(self, position: str) -> None:
        horizontal, vertical = position.split()
        self._rover_position = Position(int(horizontal), int(vertical))

    def execute(self, command: str) -> None:
        if command not in ('f', 'b'):
            raise RuntimeError(f'Unknown command: {command!r}')
        if not self._rover_position:
            raise RuntimeError("Can't move, no rover landed yet")
        if command == 'f':
            self._rover_position = self._rover_position.moved_vertically_by(1)
        else:
            self._rover_position = self._rover_position.moved_vertically_by(-1)


class TestMarsRoverApplication:

    def setup_method(self) -> None:
        self.app = MarsRoverApplication()

    def test_reports_no_rover_position_before_the_rover_landed(self) -> None:
        assert self.app.rover_position() is None

    def test_lands_rover_with_the_given_position(self) -> None:
        self.app.land_rover('3 4')
        assert self.app.rover_position() == '3 4'

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
        self.app.land_rover(initial_position)
        self.app.execute('f')
        assert self.app.rover_position() == final_position

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
        self.app.land_rover(initial_position)
        self.app.execute('b')
        assert self.app.rover_position() == final_position

    def test_can_not_move_until_the_rover_landed(self) -> None:
        with pytest.raises(RuntimeError) as error:
            self.app.execute('f')
        assert str(error.value) == "Can't move, no rover landed yet"

    def test_rejects_unknown_commands(self) -> None:
        with pytest.raises(RuntimeError) as error:
            self.app.execute('x')
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
