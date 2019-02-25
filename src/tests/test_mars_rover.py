from typing import Optional

import pytest


class Position:

    def __init__(self, horizontal: int, vertical: int) -> None:
        self._horizontal = horizontal
        self._vertical = vertical

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
        self._rover_position: Optional[str] = None

    def rover_position(self) -> Optional[str]:
        return self._rover_position

    def land_rover(self, position: str) -> None:
        self._rover_position = position

    def execute(self, command: str) -> None:
        if not self._rover_position:
            raise RuntimeError("Can't move, no rover landed yet")
        horizontal, vertical = self._rover_position.split()
        position = Position(int(horizontal), int(vertical))
        self._rover_position = f'{position.horizontal()} {position.vertical() + 1}'


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

    def test_can_not_move_until_the_rover_landed(self) -> None:
        with pytest.raises(RuntimeError) as error:
            self.app.execute('f')
        assert str(error.value) == "Can't move, no rover landed yet"


class TestPosition:

    def test_two_equal_positions(self) -> None:
        assert Position(3, 4) == Position(3, 4)

    def test_two_positions_with_different_horizontal_point(self) -> None:
        assert Position(3, 4) != Position(2, 4)

    def test_two_positions_with_different_vertical_point(self) -> None:
        assert Position(3, 4) != Position(3, 5)
