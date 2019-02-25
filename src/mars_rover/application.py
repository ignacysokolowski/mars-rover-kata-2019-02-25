import re
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
            raise UserInputError.invalid_position(user_input)
        return Position(direction, Coordinates(int(match.group(1)), int(match.group(2))))

    def _pattern(self) -> Pattern:
        return re.compile(r'^(\d+) (\d+) (?P<direction>[A-Z])$')

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
