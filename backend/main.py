from fastapi import FastAPI
from .game.game_manager import GameManager

app = FastAPI()
game_manager = GameManager()


@app.get("/")
def root():
    return {"message": "Blackjack API running"}

@app.post("/games")
def create_game(balance: int):
    game = game_manager.create_game(balance)

    return {
        "game_id": game.game_id
    }
