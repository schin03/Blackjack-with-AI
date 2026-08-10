from .card import Card

class Deck: 
    def __init__(self):
        suits = ["♦️", "♣️", "♥️", "♠️"]
        nums = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

        self.cards = []

        for suit in suits:
            for num in nums:
                if num in ["J", "Q", "K"]:
                    value = 10
                elif num == "A":
                    value = 11
                else:
                    value = int(num)
                self.cards.append(Card(suit, num, value))


    
    