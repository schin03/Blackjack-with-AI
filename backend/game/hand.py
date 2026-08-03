class Hand:
    def __init__(self):
        self.cards = []
    
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
            total += card.value

            if card.num == "A":
                aces += 1
        
        while total > 21 and aces > 0:
            total -= 10
            aces -=1
        
        return total
    
    def bust_check(self):
        return self.get_value() > 21
    
    def reveal_last(self):
        self.cards[-1].set_hidden(False)

    