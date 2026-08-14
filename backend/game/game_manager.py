import secrets

from .game_textbased import Game

class GameManager:
    def __init__(self):
        self.games = {}

    
    def create_game(self, balance):
        game_id = secrets.token_urlsafe(32)
        game = Game(game_id, balance)

        self.games[game_id] = game


    def get_game(self, game_id):
        return self.games[game_id]