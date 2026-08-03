import random
from .deck import Deck


class Shoe:
    def __init__(self):
        self.cards = []
        self.reset()

    def deal(self):
        return self.cards.pop()

    def reset(self):
        deck1 = Deck()
        deck2 = Deck()
        self.cards = deck1.cards + deck2.cards
        random.shuffle(self.cards)
    
    def cards_left(self):
        return len(self.cards)
    

