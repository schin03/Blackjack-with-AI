import random
from .deck import Deck
from .card import Card

class Shoe:
    def __init__(self):
        self.cards = []
        self.reset()

    def custom_deal(self, num, val):
        return Card("♥️", num, val)
    
    def deal(self):
        if not self.cards:
            self.reset()
        return self.cards.pop()

    def reset(self):
        deck1 = Deck()
        deck2 = Deck()
        self.cards = deck1.cards + deck2.cards
        random.shuffle(self.cards)
    
    def cards_left(self):
        return len(self.cards)
    

