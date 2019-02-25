from typing import Optional

import pytest


class MarsRoverApplication:

    def __init__(self) -> None:
        self._rover_position: Optional[str] = None

    def rover_position(self) -> Optional[str]:
        return self._rover_position

    def land_rover(self, position: str) -> None:
        self._rover_position = position

    def execute(self, command: str) -> None:
        self._rover_position = '3 5'


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
