import secrets

from .game import Game

class GameManager:
    def __init__(self):
        self.games = {}

    
    def create_game(self, balance):
        game_id = secrets.token_urlsafe(32)
        game = Game(game_id, balance)

        self.games[game_id] = game
        return game


    def get_game(self, game_id):
        return self.games[game_id]