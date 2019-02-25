import pytest

from mars_rover.domain import Coordinates
from mars_rover.domain import Direction


class Position:

    def __init__(self, direction: Direction, coordinates: Coordinates) -> None:
        self._direction = direction
        self._coordinates = coordinates

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Position):  # pragma: nocover
            return NotImplemented
        return self._direction == other._direction and self._coordinates == other._coordinates


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
            ('E', Direction.east()),
            ('W', Direction.west()),
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


class TestPosition:

    def test_two_equal_positions(self) -> None:
        assert Position(
            Direction.north(), Coordinates(2, 3)
        ) == Position(
            Direction.north(), Coordinates(2, 3)
        )

    def test_two_positions_facing_different_direction(self) -> None:
        assert Position(
            Direction.north(), Coordinates(2, 3)
        ) != Position(
            Direction.south(), Coordinates(2, 3)
        )

    def test_two_positions_with_differrent_coordinates(self) -> None:
        assert Position(
            Direction.north(), Coordinates(2, 3)
        ) != Position(
            Direction.north(), Coordinates(3, 4)
        )
