import random
from .card import Card

class Deck: 
    def __init__(self):
        suits = ["♦️", "♣️", "♥️", "♠️"]
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        self.cards = [
            Card(suit, value)
            for suit in suits
            for value in values
        ]

    def shuffle(self):
        random.shuffle(self.cards)
    
    