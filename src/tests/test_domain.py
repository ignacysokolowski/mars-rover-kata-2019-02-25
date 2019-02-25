import pytest

from mars_rover.domain import Coordinates
from mars_rover.domain import Direction
from mars_rover.domain import Position
from mars_rover.domain import Rover
from mars_rover.domain import RoverOutsideSurface


class TestCoordinates:

    def test_two_equal_coordinates(self) -> None:
        assert Coordinates(3, 4) == Coordinates(3, 4)

    def test_two_coordinates_with_different_horizontal_point(self) -> None:
        assert Coordinates(3, 4) != Coordinates(2, 4)

    def test_two_coordinates_with_different_vertical_point(self) -> None:
        assert Coordinates(3, 4) != Coordinates(3, 5)

    def test_coordinates_are_greater_if_at_least_one_dimension_is_bigger(self) -> None:
        assert Coordinates(3, 6) > Coordinates(4, 5)
        assert Coordinates(6, 3) > Coordinates(5, 4)
        assert Coordinates(3, 5) < Coordinates(4, 6)
        assert Coordinates(-1, 3) < Coordinates(0, 2)
        assert Coordinates(3, -1) < Coordinates(2, 0)


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


class TestRover:

    @pytest.mark.parametrize(
        'coordinates', [
            Coordinates(6, 3),
            Coordinates(7, 3),
            Coordinates(3, 6),
            Coordinates(3, 7),
        ],
        ids=repr
    )
    def test_can_not_land_outside_of_the_surface(self, coordinates: Coordinates) -> None:
        with pytest.raises(RoverOutsideSurface):
            Rover(Position(Direction.north(), coordinates))

    @pytest.mark.parametrize(
        ('direction', 'initial_coordinates', 'final_coordinates'), [
            (Direction.north(), Coordinates(3, 4), Coordinates(3, 5)),
            (Direction.north(), Coordinates(3, 3), Coordinates(3, 4)),
            (Direction.north(), Coordinates(2, 3), Coordinates(2, 4)),
            (Direction.south(), Coordinates(3, 4), Coordinates(3, 3)),
            (Direction.south(), Coordinates(3, 3), Coordinates(3, 2)),
            (Direction.south(), Coordinates(2, 3), Coordinates(2, 2)),
            (Direction.east(), Coordinates(3, 4), Coordinates(4, 4)),
            (Direction.west(), Coordinates(3, 4), Coordinates(2, 4)),
        ],
        ids=repr
    )
    def test_moves_forward(
            self,
            direction: Direction,
            initial_coordinates: Coordinates,
            final_coordinates: Coordinates,
    ) -> None:
        rover = Rover(Position(direction, initial_coordinates))
        rover.move_forward()
        assert rover.position() == Position(direction, final_coordinates)

    @pytest.mark.parametrize(
        ('direction', 'initial_coordinates', 'final_coordinates'), [
            (Direction.north(), Coordinates(3, 4), Coordinates(3, 3)),
            (Direction.north(), Coordinates(3, 3), Coordinates(3, 2)),
            (Direction.north(), Coordinates(2, 3), Coordinates(2, 2)),
            (Direction.south(), Coordinates(3, 4), Coordinates(3, 5)),
            (Direction.south(), Coordinates(3, 3), Coordinates(3, 4)),
            (Direction.south(), Coordinates(2, 3), Coordinates(2, 4)),
            (Direction.east(), Coordinates(3, 4), Coordinates(2, 4)),
            (Direction.west(), Coordinates(3, 4), Coordinates(4, 4)),
        ],
        ids=repr
    )
    def test_moves_backward(
            self,
            direction: Direction,
            initial_coordinates: Coordinates,
            final_coordinates: Coordinates,
    ) -> None:
        rover = Rover(Position(direction, initial_coordinates))
        rover.move_backward()
        assert rover.position() == Position(direction, final_coordinates)

    @pytest.mark.parametrize(
        'position', [
            Position(Direction.north(), Coordinates(3, 5)),
            Position(Direction.east(), Coordinates(5, 3)),
            Position(Direction.south(), Coordinates(3, 0)),
            Position(Direction.west(), Coordinates(0, 3)),
        ],
        ids=repr
    )
    def test_does_not_move_forward_outside_the_surface(self, position: Position) -> None:
        rover = Rover(position)
        rover.move_forward()
        assert rover.position() == position

    @pytest.mark.parametrize(
        'position', [
            Position(Direction.north(), Coordinates(3, 0)),
            Position(Direction.east(), Coordinates(0, 3)),
            Position(Direction.south(), Coordinates(3, 5)),
            Position(Direction.west(), Coordinates(5, 3)),
        ],
        ids=repr
    )
    def test_does_not_move_backward_outside_the_surface(self, position: Position) -> None:
        rover = Rover(position)
        rover.move_backward()
        assert rover.position() == position

    @pytest.mark.parametrize(
        ('initial_direction', 'final_direction'), [
            (Direction.north(), Direction.east()),
            (Direction.east(), Direction.south()),
            (Direction.south(), Direction.west()),
            (Direction.west(), Direction.north()),
        ],
        ids=repr
    )
    def test_turns_right(self, initial_direction: Direction, final_direction: Direction) -> None:
        rover = Rover(Position(initial_direction, Coordinates(3, 3)))
        rover.turn_right()
        assert rover.position() == Position(final_direction, Coordinates(3, 3))

    @pytest.mark.parametrize(
        ('initial_direction', 'final_direction'), [
            (Direction.north(), Direction.west()),
            (Direction.west(), Direction.south()),
            (Direction.south(), Direction.east()),
            (Direction.east(), Direction.north()),
        ],
        ids=repr
    )
    def test_turns_left(self, initial_direction: Direction, final_direction: Direction) -> None:
        rover = Rover(Position(initial_direction, Coordinates(3, 3)))
        rover.turn_left()
        assert rover.position() == Position(final_direction, Coordinates(3, 3))
