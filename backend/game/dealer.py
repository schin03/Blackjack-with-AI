from .hand import Hand
from .states.hand_state import HandState

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def blackjack_check(self):
        if self.hand.blackjack_check():
            self.hand.state = HandState.BLACKJACK

    def dealer_draw(self, shoe):
        self.hand.reveal_last()
        
        while (self.hand.get_value() < 17):
            self.hand.add_card(shoe.deal())
        
        if self.hand.get_value() > 21:
            self.hand.state = HandState.BUST
        else:
            self.hand.state  = HandState.STAND

    def player_bust(self):
        self.hand.reveal_last()
    
    def dealer_reset(self):
        self.hand = Hand()
        
    def upcard_ace(self):
        return self.hand[0].value == 11