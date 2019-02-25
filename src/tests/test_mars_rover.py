import pytest

from mars_rover.application import MarsRoverApplication
from mars_rover.application import UserInputError
from mars_rover.coordinates import Coordinates
from mars_rover.direction import Direction


class TestMarsRoverApplication:

    def land_rover_with_position(self, position: str) -> MarsRoverApplication:
        return MarsRoverApplication.landing_with(position)

    @pytest.mark.parametrize(
        'position', [
            '3 4 N',
            '2 3 N',
            '3 4 S',
            '3 4 E',
            '3 4 W',
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
            ('3 4 E', '4 4 E'),
            ('3 4 W', '2 4 W'),
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
            ('3 4 E', '2 4 E'),
            ('3 4 W', '4 4 W'),
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

    @pytest.mark.parametrize(
        ('initial_direction', 'final_direction'), [
            ('N', 'E'),
            ('E', 'S'),
            ('S', 'W'),
            ('W', 'N'),
        ]
    )
    def test_turns_rover_right(self, initial_direction: str, final_direction: str) -> None:
        app = self.land_rover_with_position('3 4 ' + initial_direction)
        app.execute('r')
        assert app.rover_position() == '3 4 ' + final_direction

    @pytest.mark.parametrize(
        ('initial_direction', 'final_direction'), [
            ('N', 'W'),
            ('W', 'S'),
            ('S', 'E'),
            ('E', 'N'),
        ]
    )
    def test_turns_rover_left(self, initial_direction: str, final_direction: str) -> None:
        app = self.land_rover_with_position('3 4 ' + initial_direction)
        app.execute('l')
        assert app.rover_position() == '3 4 ' + final_direction

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
