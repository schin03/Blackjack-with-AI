from .deck import Deck

class Game:
    def play(self):
        deck = Deck()
        print("cards: \n")
        print(deck.cards)

        print("Player Cards: ")
        print("\nDealer cards: ")