from .hand import Hand
from .states.hand_state import HandState

class Dealer:
    def __init(self):
        self.hand = Hand()
        self.state = HandState.ACTIVE

    def blackjack_check(self):
        if self.hand.blackjack_check():
            self.state = HandState.BLACKJACK

    def dealer_draw(self, shoe):
        self.hand.reveal_last()
        
        while (self.hand.get_value() < 17):
            self.hand.add_card(shoe.deal())
        
        if self.hand.get_value() > 21:
            self.state = HandState.BUST
        else:
            self.state = HandState.STAND