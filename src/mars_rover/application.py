import re

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


class MarsRoverApplication:

    @classmethod
    def landing_with(cls, rover_position: str) -> 'MarsRoverApplication':
        match = re.match(r'^(\d+) (\d+) ([A-Z])$', rover_position)
        if not match:
            raise UserInputError.invalid_position(rover_position)
        try:
            direction = Direction.for_symbol(match.group(3))
        except ValueError:
            raise UserInputError.invalid_position(rover_position)
        position = Position(direction, Coordinates(int(match.group(1)), int(match.group(2))))
        return cls(position.coordinates(), position.direction())

    def __init__(self, rover_coordinates: Coordinates, rover_direction: Direction) -> None:
        self._rover = Rover(rover_coordinates, rover_direction)

    def rover_position(self) -> str:
        position = Position(self._rover.direction(), self._rover.coordinates())
        return (
            f'{position.coordinates().horizontal()} '
            f'{position.coordinates().vertical()} '
            f'{position.direction().symbol()}'
        )

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
