from typing import Optional


class MarsRoverApplication:

    def rover_position(self) -> Optional[str]:
        return None


class TestMarsRoverApplication:

    def test_reports_no_rover_position_before_the_rover_landed(self) -> None:
        app = MarsRoverApplication()
        assert app.rover_position() is None
