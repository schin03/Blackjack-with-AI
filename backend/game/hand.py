from hand_state import HandState
class Hand:
    def __init__(self):
        self.cards = []
        self.state = HandState.ACTIVE
    
    def __str__(self):
        return ", ".join(str(card.get_card_val()) for card in self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        total = 0
        aces = 0
        for card in self.cards:
            if card.get_hidden() == True:
                continue
            total += int(card.value)

            if card.num == "A":
                aces += 1
        
        while total > 21 and aces > 0:
            total -= 10
            aces -=1
        
        return total
    
    def bust_check(self):
        return self.get_value() > 21
    
    def split_check(self):
        if len(self.cards) != 2:
            return False
        card_1 = self.cards[0]
        card_2 = self.cards[1]
        return card_1.value == card_2.value
          

    def reveal_last(self):
        self.cards[-1].set_hidden(False)

    