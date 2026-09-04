from game.shoe import Shoe
from game.player import Player
from game.dealer import Dealer
from game.hand import Hand
from game.errors.blackjack_errors import IncorrectState, InsufficientFundsError
from game.states.hand_state import HandState
from game.states.game_state import GameState


class Game:
    def __init__(self, game_id, balance):
        self.game_id = game_id
        self.shoe = Shoe()
        self.player = Player(balance)
        self.dealer = Dealer()
        self.game_state = GameState.INACTIVE
        self.current_hand = 0

    def deal(self, bet):
        if self.shoe.cards_left() < 25:
            self.shoe.reset()
        
        self.dealer.dealer_reset()
        self.player.player_reset()
        
        self.current_hand = 0

        self.player.choose_bet(bet)
        
        self.game_state = GameState.ACTIVE

        self.player.add_hand(Hand(bet))
        self.player.hands[0].add_card(self.shoe.deal())
        self.dealer.hand.add_card(self.shoe.deal())
        self.player.hands[0].add_card(self.shoe.deal())

        hidden_card = self.shoe.deal()
        hidden_card.set_hidden(True)
        self.dealer.hand.add_card(hidden_card)
        
        self.dealer.blackjack_check()
        self.player.blackjack_check()
        
        if self.dealer.upcard_ace():
            self.game_state = GameState.INSURANCE
            return
        
        
        if self.player.hands[0].state == HandState.BLACKJACK:
            self.game_state = GameState.PLAYER_BLACKJACK
            self.dealer.hide_last(False)
            self.payout_helper(self.player.hands[self.current_hand])
        
        
    def insurance_choice(self, choice):
        # current dealer hand should have up-card A
        if self.game_state != GameState.INSURANCE:
            raise IncorrectState("current state is not set as INSURANCE")
        
        self.player.insurance_choice(choice)
        if self.dealer.hand.state == HandState.BLACKJACK:
            # if dealer bj
            self.dealer.hide_last(False)
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
                self.player.balance += self.player.current_bet/2
                self.game_state = GameState.PLAYER_WIN
            else:
                self.game_state = GameState.PLAYER_PUSH
        else:
            if self.player.hands[0].state == HandState.BLACKJACK:
                self.game_state = GameState.PLAYER_PUSH
            else:
                self.game_state = GameState.DEALER_WIN
        self.payout_helper(self.player.hands[self.current_hand])

    def dealerAceNoBJ(self):
        # can return state of ACTIVE having just dealt with player's choice of insurance
        if self.player.hands[0].state == HandState.BLACKJACK:
            self.game_state = GameState.PLAYER_BLACKJACK
            self.dealer.hide_last(False)
            self.payout_helper(self.player.hands[self.current_hand])
        else:
            self.game_state = GameState.ACTIVE


    def hit(self):
        if self.game_state != GameState.ACTIVE:
            raise IncorrectState("current state is not set as ACTIVE")

        self.player.hit(self.current_hand, self.shoe)
        
        if self.player.hands[self.current_hand].state == HandState.BUST:
            self.finish_current_hand(HandState.BUST)
    
    def double(self):
        if self.game_state != GameState.ACTIVE:
            raise IncorrectState("current state is not set as ACTIVE")
        
        self.player.double(self.current_hand, self.shoe)

        final_state = (
            HandState.BUST 
            if self.player.hands[self.current_hand].state == HandState.BUST
            else HandState.DOUBLE
        )

        self.finish_current_hand(final_state)

    def split(self):
        if self.game_state != GameState.ACTIVE:
            raise IncorrectState("current state is not set as ACTIVE") 

        self.player.split(self.current_hand)
        
        # deal the second card to the first split hand
        self.player.hands[self.current_hand].add_card(self.shoe.deal())
    
    def stand(self):
        if self.game_state != GameState.ACTIVE:
            raise IncorrectState("current state is not set as ACTIVE")
        
        self.finish_current_hand(HandState.STAND)

    def next_hand(self):
            self.current_hand += 1
            
            # move onto the next hand, deal a card
            if self.current_hand < len(self.player.hands):
                self.player.hands[self.current_hand].add_card(self.shoe.deal())
                self.game_state = GameState.ACTIVE
            else:
                self.dealer_action()

    def finish_current_hand(self, state):
        self.player.hands[self.current_hand].state = state
        self.next_hand()
    
    def dealer_action(self):
        self.dealer.hide_last(False)

        if any (hand.state != HandState.BUST for hand in self.player.hands):
            self.dealer.dealer_draw(self.shoe)

        dealer_bust = self.dealer.hand.bust_check()
        dealer_value = self.dealer.hand.get_value()

        self.game_state = GameState.DEALER_WIN

        for hand in self.player.hands:
            hand_value = hand.get_value()
            if hand.state == HandState.BUST:
                continue
            if hand.state == HandState.STAND:
                if dealer_bust or dealer_value < hand_value:
                    self.game_state = GameState.PLAYER_WIN
                elif dealer_value == hand_value:
                    self.game_state = GameState.PLAYER_PUSH
            elif hand.state == HandState.DOUBLE:
                if dealer_bust or dealer_value < hand_value:
                    self.game_state = GameState.PLAYER_DOUBLE_WIN
                elif dealer_value == hand_value:
                    self.game_state = GameState.PLAYER_DOUBLE_PUSH
            
            self.payout_helper(hand)
    
        
    def payout_helper(self, hand):
        bet = hand.bet
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
        
        

    
    

    
