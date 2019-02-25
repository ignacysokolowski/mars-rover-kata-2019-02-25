import pytest

from mars_rover.application import MarsRoverApplication
from mars_rover.application import UserInputError


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
        'direction', [
            '5',
            'NS',
            'A',
        ]
    )
    def test_rejects_invalid_initial_direction(self, direction: str) -> None:
        with pytest.raises(UserInputError) as error:
            self.land_rover_with_position('3 4 ' + direction)
        assert str(error.value) == 'Invalid direction: ' + direction

    def test_moves_rover_forward(self) -> None:
        app = self.land_rover_with_position('3 4 N')
        app.execute('f')
        assert app.rover_position() == '3 5 N'

    @pytest.mark.parametrize(
        'position', [
            '3 0 S',
            '0 3 W',
        ]
    )
    def test_does_not_move_forward_to_negative_position(self, position: str) -> None:
        app = self.land_rover_with_position(position)
        app.execute('f')
        assert app.rover_position() == position

    def test_moves_rover_backward(self) -> None:
        app = self.land_rover_with_position('3 4 N')
        app.execute('b')
        assert app.rover_position() == '3 3 N'

    def test_turns_rover_right(self) -> None:
        app = self.land_rover_with_position('3 4 N')
        app.execute('r')
        assert app.rover_position() == '3 4 E'

    def test_turns_rover_left(self) -> None:
        app = self.land_rover_with_position('3 4 N')
        app.execute('l')
        assert app.rover_position() == '3 4 W'

    def test_rejects_unknown_commands(self) -> None:
        app = self.land_rover_with_position('3 4 N')
        with pytest.raises(UserInputError) as error:
            app.execute('x')
        assert str(error.value) == "Unknown command: 'x'"
