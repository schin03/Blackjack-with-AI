from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from game.errors.blackjack_errors import InsufficientFundsError, InvalidHandError, IncorrectState
from game.game_manager import GameManager
from game.states.hand_state import HandState

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173",
                     "https://blackjack-with-ai.vercel.app"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

game_manager = GameManager()
class DealHand(BaseModel):
    bet: float

class InsuranceChoice(BaseModel):
    choice: bool

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
                    "cards": hand.cards,
                    "value": hand.get_value(),
                    "state": hand.state,
                    "can_double" : hand.state == HandState.ACTIVE
                }
                for hand in game.player.hands
                ],
                "current_bal": game.player.balance,
                "current_bet": game.player.current_bet
            },
            "dealer": {
                "cards": game.dealer.hand.cards,
                "value": game.dealer.hand.get_value(),
                "state": game.dealer.hand.state
            },
            "game_state": game.game_state
        }
    
    except InsufficientFundsError as e:
        raise HTTPException(
            status_code = 400,
            detail=str(e)
        )
@app.post("/games/{game_id}/insurance")
def insurance(game_id: str, req: InsuranceChoice):
    game = game_manager.get_game(game_id)
    try:
        game.insurance_choice(req.choice)
    except IncorrectState as e:
        raise HTTPException(
            status_code = 400,
            detail = str(e)
        )
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": hand.cards,
                "value": hand.get_value(),
                "state": hand.state,
                "can_double" : hand.state == HandState.ACTIVE
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": game.dealer.hand.cards,
            "value": game.dealer.hand.get_value(),
            "state": game.dealer.hand.state
        },
        "game_state": game.game_state
    }

@app.post("/games/{game_id}/hit")
def hit(game_id: str):
    game = game_manager.get_game(game_id)
    
    try: 
        game.hit()
    except IncorrectState as e:
        raise HTTPException(
            status_code = 400,
            detail = str(e)
        ) 
    
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": hand.cards,
                "value": hand.get_value(),
                "state": hand.state,
                "can_double" : hand.state == HandState.ACTIVE
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": game.dealer.hand.cards,
            "value": game.dealer.hand.get_value(),
            "state": game.dealer.hand.state
        },
        "game_state": game.game_state
    }

@app.post("/games/{game_id}/double")
def double(game_id: str):
    game = game_manager.get_game(game_id)
    try:
        game.double()
    except InsufficientFundsError or IncorrectState or InvalidHandError as e:
         raise HTTPException(
            status_code = 400,
            detail=str(e)
        )
         
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": hand.cards,
                "value": hand.get_value(),
                "state": hand.state,
                "can_double" : hand.state == HandState.ACTIVE
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": game.dealer.hand.cards,
            "value": game.dealer.hand.get_value(),
            "state": game.dealer.hand.state
        },
        "game_state": game.game_state
    }

@app.post("/games/{game_id}/split")
def split(game_id: str):
    game = game_manager.get_game(game_id)
    try:
        game.split()
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
                "cards": hand.cards,
                "value": hand.get_value(),
                "state": hand.state,
                "can_double" : hand.state == HandState.ACTIVE
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": game.dealer.hand.cards,
            "value": game.dealer.hand.get_value(),
            "state": game.dealer.hand.state
        },
        "game_state": game.game_state
    }

@app.post("/games/{game_id}/stand")
def stand(game_id: str):
    game = game_manager.get_game(game_id)
    game.stand()
    
    return {
        "game_id": game_id,
        "player": {
            "hands": [{
                "cards": hand.cards,
                "value": hand.get_value(),
                "state": hand.state,
                "can_double" : hand.state == HandState.ACTIVE
            }
            for hand in game.player.hands
            ],
            "current_bal": game.player.balance,
            "current_bet": game.player.current_bet
        },
        "dealer": {
            "cards": game.dealer.hand.cards,
            "value": game.dealer.hand.get_value(),
            "state": game.dealer.hand.state
        },
        "game_state": game.game_state
    }

