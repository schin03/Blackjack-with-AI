from game.hand import Hand
from game.states.hand_state import HandState

class Dealer:
    def __init__(self):
        self.hand = Hand()

    def blackjack_check(self):
        if self.hand.dealer_blackjack_check():
            self.hand.state = HandState.BLACKJACK

    def dealer_draw(self, shoe):
        self.hand.hide_last(False)
        
        while (self.hand.get_value() < 17):
            self.hand.add_card(shoe.deal())
        
        if self.hand.get_value() > 21:
            self.hand.state = HandState.BUST
        else:
            self.hand.state  = HandState.STAND

    def hide_last(self, bool):
        self.hand.hide_last(bool)
    
    def dealer_reset(self):
        self.hand = Hand()
        
    def upcard_ace(self):
        return self.hand.cards[0].value == 11