from typing import Optional


class MarsRoverApplication:

    def __init__(self) -> None:
        self._rover_position: Optional[str] = None

    def rover_position(self) -> Optional[str]:
        return self._rover_position

    def land_rover(self, position: str) -> None:
        self._rover_position = position


class TestMarsRoverApplication:

    def test_reports_no_rover_position_before_the_rover_landed(self) -> None:
        app = MarsRoverApplication()
        assert app.rover_position() is None

    def test_lands_rover_with_the_given_position(self) -> None:
        app = MarsRoverApplication()
        app.land_rover('3 4')
        assert app.rover_position() == '3 4'
