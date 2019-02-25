import re
from typing import Match
from typing import Pattern

from mars_rover.domain import Coordinates
from mars_rover.domain import Direction
from mars_rover.domain import Position
from mars_rover.domain import Rover


class UserInputError(Exception):

    @classmethod
    def invalid_position(cls, position: str) -> 'UserInputError':
        return cls(f'Invalid position: {position}')

    @classmethod
    def invalid_direction(cls, direction: str) -> 'UserInputError':
        return cls(f'Invalid direction: {direction}')

    @classmethod
    def unknown_command(cls, command: str) -> 'UserInputError':
        return cls(f'Unknown command: {command!r}')


class PositionFormat:

    def position_from(self, user_input: str) -> Position:
        match = self._pattern().match(user_input)
        if not match:
            raise UserInputError.invalid_position(user_input)
        try:
            direction = Direction.for_symbol(match.group('direction'))
        except ValueError:
            raise UserInputError.invalid_direction(match.group('direction'))
        return Position(direction, self._coordinates_from(match))

    def _pattern(self) -> Pattern:
        return re.compile(
            r'^(?P<horizontal>\d+) '
            r'(?P<vertical>\d+) '
            r'(?P<direction>.*)'
        )

    def _coordinates_from(self, match: Match) -> Coordinates:
        return Coordinates(
            int(match.group('horizontal')),
            int(match.group('vertical')),
        )

    def output_from(self, position: Position) -> str:
        return (
            f'{position.coordinates().horizontal()} '
            f'{position.coordinates().vertical()} '
            f'{position.direction().symbol()}'
        )


class MarsRoverApplication:

    @classmethod
    def landing_with(cls, rover_position: str) -> 'MarsRoverApplication':
        return cls(PositionFormat().position_from(rover_position))

    def __init__(self, position: Position) -> None:
        self._rover = Rover(position)

    def rover_position(self) -> str:
        return PositionFormat().output_from(self._rover.position())

    def execute(self, command: str) -> None:
        if command == 'f':
            self._rover.move_forward()
        elif command == 'b':
            self._rover.move_backward()
        elif command == 'r':
            self._rover.turn_right()
        elif command == 'l':
            self._rover.turn_left()
        else:
            raise UserInputError.unknown_command(command)
