from .shoe import Shoe
from .player import Player
from .dealer import Dealer
from .hand import Hand
from .errors.blackjack_errors import IncorrectState
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
        self.game_state = GameState.ACTIVE

        self.player.add_hand(Hand())
        self.player.hands[0].add_card(self.shoe.deal())
        self.dealer.hand.add_card(self.shoe.custom_deal("A", 11))
        self.player.hands[0].add_card(self.shoe.deal())

        hidden_card = self.shoe.custom_deal("9", 9)
        hidden_card.set_hidden(True)
        self.dealer.hand.add_card(hidden_card)
        
        self.dealer.blackjack_check()
        self.player.blackjack_check()
        
        if self.dealer.upcard_ace():
            self.game_state = GameState.INSURANCE
            return
        
        
        if self.player.hands[0].state == HandState.BLACKJACK:
            self.game_state = GameState.PLAYER_BLACKJACK
            self.dealer_action()
        
        
    def insurance_choice(self, choice):
        # current dealer hand should have up-card A
        if self.game_state != GameState.INSURANCE:
            raise IncorrectState("current state is not set as INSURANCE")
        
        self.player.insurance_choice(choice)
        if self.dealer.hand.state == HandState.BLACKJACK:
            # if dealer bj
            self.dealer.reveal_last()
            if choice == True:
                self.game_state = GameState.DEALER_BLACKJACK_YES
            else:
                self.game_state = GameState.DEALER_BLACKJACK_NO
            self.dealerAceBJ()
        else: 
            self.dealerAceNoBJ()

    def dealerAceBJ(self):
        # method guarantees end of hand, since dealer here has a BJ and should not continue
        if self.game_state == GameState.DEALER_BLACKJACK_YES:
            if self.player.hands[0].state == HandState.BLACKJACK:
                self.game_state = GameState.PLAYER_WIN
            else:
                self.game_state = GameState.PLAYER_PUSH
        else:
            if self.player.hands[0].state == HandState.BLACKJACK:
                self.game_state = GameState.PLAYER_PUSH
            else:
                self.game_state = GameState.DEALER_WIN
        self.handle_game_result()

    def dealerAceNoBJ(self):
        # can return state of ACTIVE having just dealt with player's choice of insurance
        if self.player.hands[0].state == HandState.BLACKJACK:
            self.game_state = GameState.PLAYER_BLACKJACK
            self.handle_game_result()
        else:
            self.game_state = GameState.ACTIVE


    def hit(self, hand_index):
        if self.game_state != GameState.ACTIVE:
            raise IncorrectState("current state is not set as ACTIVE")

        self.player.hit(hand_index, self.shoe)
        if self.player.hands[0].state == HandState.BUST:
            self.dealer_action(True)
    
    def double(self, hand_index):
        if self.game_state != GameState.ACTIVE:
            raise IncorrectState("current state is not set as ACTIVE")
        self.player.double(hand_index, self.shoe)
        state = self.player.hands[0].state == HandState.BUST
        self.game_state = GameState.PLAYER_DOUBLE
        self.dealer_action(state)

    def split(self, hand_index):
        self.player.split(hand_index)
    
    def dealer_action(self, bustcheck):
        if bustcheck or self.game_state == GameState.PLAYER_BLACKJACK:
            self.dealer.reveal_last()
            if bustcheck:
                self.game_state = GameState.DEALER_WIN
        else:
            self.dealer.dealer_draw(self.shoe)

        self.handle_game_result()
        
    def handle_game_result(self):
        if self.game_state != GameState.DEALER_WIN:
            if (
                self.dealer.hand.bust_check() == True
                or self.player.hands[0].get_value() > self.dealer.hand.get_value()
            ):
                if self.game_state == GameState.PLAYER_DOUBLE:
                    self.game_state = GameState.PLAYER_DOUBLE_WIN
                else:
                    self.game_state = GameState.PLAYER_WIN
                    
            elif self.player.hands[0].get_value() == self.dealer.hand.get_value():
                if self.game_state == GameState.PLAYER_DOUBLE:
                    self.game_state = GameState.PLAYER_DOUBLE_PUSH
                else:
                    self.game_state = GameState.PLAYER_PUSH
                    
            else:
                self.game_state = GameState.DEALER_WIN

        self.payout_helper()
        
    def payout_helper(self):
        bet = self.player.current_bet
        if self.game_state == GameState.PLAYER_BLACKJACK:
            self.player.balance += bet * 2.5
        elif self.game_state == GameState.PLAYER_DOUBLE_WIN:
            self.player.balance += bet * 4
        elif self.game_state == GameState.PLAYER_WIN:
            self.player.balance += bet * 2
        elif self.game_state == GameState.PLAYER_PUSH:
            self.player.balance += bet
        elif self.game_state == GameState.PLAYER_DOUBLE_PUSH:
            self.player.balance += bet * 2
        
        

    
    

    
