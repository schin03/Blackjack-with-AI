from fastapi import FastAPI
from fastapi import HTTPException
from .game.errors.blackjack_errors import InsufficientFundsError, InvalidHandError
from pydantic import BaseModel
from .game.game_manager import GameManager

app = FastAPI()
game_manager = GameManager()
class DealHand(BaseModel):
    bet: float

@app.get("/")
def root():
    return {"message": "Blackjack API running"}

@app.post("/games")
def create_game(balance: int):
    game = game_manager.create_game(balance)
    return {
        "game_id": game.game_id
        
    }

@app.post("/games/{game_id}/deal")
def deal(game_id: str, request: DealHand):
    try:
        game = game_manager.get_game(game_id)
        game.deal(request.bet)
        
        return {
            "game_id": game_id,
            "player": {
                "hands": [{
                    "cards": str(hand),
                    "value": hand.get_value()
                }
                for hand in game.player.hands
                ],
                "current_bal": game.player.balance,
                "current_bet": game.player.current_bet
            },
            "dealer": {
                "cards": str(game.dealer.hand),
                "value": game.dealer.hand.get_value()
            },
            "game_active": game.game_active
        }
    
    except InsufficientFundsError as e:
        raise HTTPException(
            status_code = 400,
            detail=str(e)
        )

@app.post("/games/{game_id}/hit")
def hit(game_id: str):
    game = game_manager.get_game(game_id)
    game.hit(0)
    
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": str(hand),
                "value": hand.get_value()
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": str(game.dealer.hand),
            "value": game.dealer.hand.get_value()
        },
        "game_active": game.game_active
    }

@app.post("/games/{game_id}/double")
def double(game_id: str):
    game = game_manager.get_game(game_id)
    try:
        game.double(0)
    except InsufficientFundsError as e:
         raise HTTPException(
            status_code = 400,
            detail=str(e)
        )
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": str(hand),
                "value": hand.get_value()
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": str(game.dealer.hand),
            "value": game.dealer.hand.get_value()
        },
        "game_active": game.game_active
    }

@app.post("/games/{game_id}/split")
def split(game_id: str):
    game = game_manager.get_game(game_id)
    try:
        game.split(0)
    except InsufficientFundsError as e:
         raise HTTPException(
            status_code = 400,
            detail = str(e)
        )
    except InvalidHandError as e:
        raise HTTPException(
            status_code = 400,
            detail = str(e)
        )
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": str(hand),
                "value": hand.get_value()
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": str(game.dealer.hand),
            "value": game.dealer.hand.get_value()
        },
        "game_active": game.game_active
    }

@app.post("/games/{game_id}/stand")
def stand(game_id: str):
    game = game_manager.get_game(game_id)
    game.dealer_action(False)
    
    return {
        "game_id": game_id,
        "player": {
            "cards": str(game.player.hands[0]),
            "value": game.player.hands[0].get_value()
        },
        "dealer": {
            "cards": str(game.dealer.hand),
            "value": game.dealer.hand.get_value()
        },
        "game_active": game.game_active
    }

