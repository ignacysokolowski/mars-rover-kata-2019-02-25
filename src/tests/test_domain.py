import pytest

from mars_rover.domain import Coordinates
from mars_rover.domain import Direction


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
