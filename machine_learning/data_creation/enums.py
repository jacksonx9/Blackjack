from enum import Enum


class Outcome(Enum):
    WIN = 1
    LOSS = 0
    INVALID = -1


class Move(Enum):
    STAND = 0
    HIT = 1
