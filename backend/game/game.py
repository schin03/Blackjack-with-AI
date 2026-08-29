from .shoe import Shoe
from .player import Player
from .dealer import Dealer
from .hand import Hand
from .states.hand_state import HandState
from .states.game_state import GameState


class Game:
    def __init__(self, game_id, balance):
        self.game_id = game_id
        self.shoe = Shoe()
        self.player = Player(balance)
        self.dealer = Dealer()
        self.game_state = GameState.INACTIVE

    def deal(self, bet):
        self.dealer.dealer_reset()
        self.player.player_reset()
        
        self.player.choose_bet(bet)
        self.game_active = GameState.ACTIVE

        self.player.add_hand(Hand())
        self.player.hands[0].add_card(self.shoe.deal())
        self.dealer.hand.add_card(self.shoe.deal())
        self.player.hands[0].add_card(self.shoe.deal())

        hidden_card = self.shoe.deal()
        hidden_card.set_hidden(True)
        self.dealer.hand.add_card(hidden_card)
        
        if self.dealer.upcard_ace():
            self.game_state == GameState.INSURANCE
        self.dealer.blackjack_check()
        self.player.blackjack_check()
        

    
    def hit(self, hand_index):
        self.player.hit(hand_index, self.shoe)
        if self.player.hands[0].state == HandState.BUST:
            self.dealer_action(True)
    
    def double(self, hand_index):
        self.player.double(hand_index, self.shoe)
        state = self.player.hands[0].state == HandState.BUST
        self.dealer_action(state)

    def split(self, hand_index):
        self.player.split(hand_index)
    
    def dealer_action(self, bustcheck):
        if bustcheck:
            self.dealer.player_bust()
        else:
            self.dealer.dealer_draw(self.shoe)
        self.game_active = GameState.INACTIVE
        
    
    
    

    
