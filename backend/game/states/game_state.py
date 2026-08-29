from enum import Enum

class GameState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PLAYER_TURN = "player_turn"
    DEALER_TURN = "dealer_turn"
    INSURANCE = "insurance"

    