class Card: 
    def __init__(self, suit, num, value):
        self.suit = suit
        self.num = num
        self.value = value
        self.icon = suit
        self.hidden = False    

    def __str__(self):
        return f"{self.suit}{self.num}"
    
    def __repr__(self):
        return str(self)

    def set_hidden(self, state):
        self.hidden = state
        self.icon = "⍰" if state else self.suit

    def get_hidden(self):
        return self.hidden

    def get_card_val(self):
        if self.hidden:
            return f"{self.icon}"
        else:
            return f"{self.suit}{self.num}"