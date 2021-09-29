from enum import Enum


class Actions(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    NOOP = 'NOOP'
    TELEPORT = 'TELEPORT'
    TRAP = 'TRAP'
