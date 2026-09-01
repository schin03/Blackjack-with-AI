from enum import Enum

class HandState(Enum):
    ACTIVE = "active"
    HIT = "hit"
    STAND = "stand"
    BUST = "bust"
    BLACKJACK = "blackjack"
    