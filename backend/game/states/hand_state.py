from enum import Enum

class HandState(Enum):
    ACTIVE = "active"
    HIT = "hit"
    DOUBLE = "double"
    STAND = "stand"
    BUST = "bust"
    BLACKJACK = "blackjack"