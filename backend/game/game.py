from .shoe import Shoe
from .player import Player
from .dealer import Dealer
from .hand import Hand

class Game:
    def __init__(self, game_id, balance):
        self.game_id = game_id
        self.shoe = Shoe()
        self.player = Player(balance)
        self.dealer = Dealer()
        self.game_active = False

    
    def start(self, bet):
        self.player.choose_bet(bet)
        self.game_active = True

        self.player.add_hand(Hand())
        self.player.hands[0].add_card(self.shoe.deal())
        self.dealer.hand.add_card(self.shoe.deal())
        self.player.hands[0].add_card(self.shoe.deal())

        hidden_card = self.shoe.deal()
        hidden_card.set_hidden(True)
        self.dealer.hand.add_card(hidden_card)

    
    def hit(self, hand_index):
        self.player.hit(hand_index, self.shoe)
    
    def double(self, hand_index):
        self.player.double(hand_index, self.shoe)

    def split(self, hand_index):
        self.player.split(hand_index)
    
    

    
