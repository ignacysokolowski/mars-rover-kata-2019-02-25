class Step:

    def __init__(self, points_east: int, points_north: int) -> None:
        self._points_east = points_east
        self._points_north = points_north

    def points_east(self) -> int:
        return self._points_east

    def points_north(self) -> int:
        return self._points_north
