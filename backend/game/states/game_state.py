from enum import Enum

class GameState(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    INSURANCE = "insurance"
    PLAYER_DOUBLE = "player_double"

    # 5 game-ending states to conclude hand
    PLAYER_DOUBLE_WIN = "player_double_win"
    PLAYER_DOUBLE_PUSH = "player_double_win"
    PLAYER_WIN = "player_win"
    PLAYER_BLACKJACK = "player_blackjack"
    PLAYER_PUSH = "player_push"
    DEALER_WIN = "dealer_win"

    # yes/no for insurance
    DEALER_BLACKJACK_NO = "dealer_blackjack_no"
    DEALER_BLACKJACK_YES = "dealer_blackjack_yes"

    