class Card: 
    def __init__(self, suit, num, value):
        self.suit = suit
        self.num = num
        self.value = value
    
    def __str__(self):
        return f"{self.suit}{self.num}"
    
    def __repr__(self):
        return str(self)