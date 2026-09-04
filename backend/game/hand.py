from game.states.hand_state import HandState
class Hand:
    def __init__(self, bet = 0, is_split = False):
        self.cards = []
        self.bet = bet
        self.is_split = is_split
        self.state = HandState.ACTIVE
    
    def __str__(self):
        return ", ".join(str(card.get_card_val()) for card in self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        total = 0
        aces = 0
        for card in self.cards:
            if card.hidden == True:
                continue
            total += int(card.value) 
            if card.num == "A":
                aces += 1
        
        while total > 21 and aces > 0:
            total -= 10
            aces -=1
        
        return total
    
    def blackjack_check(self):
        return self.get_value() == 21 and len(self.cards) == 2

    def dealer_blackjack_check(self):
        self.hide_last(False)
        bool = self.blackjack_check()
        self.hide_last(True)
        return bool

    def hide_last(self, bool):
            self.cards[-1].set_hidden(bool)

    def bust_check(self):
        return self.get_value() > 21
    
    def split_check(self):
        if len(self.cards) != 2:
            return False
        card_1 = self.cards[0]
        card_2 = self.cards[1]
        return card_1.value == card_2.value
          
    def can_split(self):
        return self.state == HandState.ACTIVE and self.split_check()

    