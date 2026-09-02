from game.hand import Hand
from game.states.hand_state import HandState
from game.errors.blackjack_errors import InsufficientFundsError, InvalidHandError

class Player:
    def __init__(self, bal):
        self.hands = []
        self.balance = bal
        self.current_bet = 0
        self.insurance = False

    def blackjack_check(self):
        if self.hands[0].blackjack_check():
            self.hands[0].state = HandState.BLACKJACK

    def choose_bet(self, bet_amount):
        if bet_amount > self.balance:
            raise InsufficientFundsError("Insufficient Funds")
        else:
            self.current_bet = bet_amount
            self.balance -= bet_amount

    def add_hand(self, hand):
        self.hands.append(hand)

    def hit(self, hand_index, shoe):
        card = shoe.deal()
        curr_hand = self.hands[hand_index]
        curr_hand.add_card(card)
        curr_hand.state = HandState.HIT

        # if current hand's value is > 21, update hand validity state
        if curr_hand.bust_check():
            curr_hand.state = HandState.BUST
    
    def double(self, hand_index, shoe):
        if self.balance - self.current_bet < 0:
            raise InsufficientFundsError("Insufficient Funds")
        self.balance -= self.current_bet
        self.hit(hand_index, shoe)
    
    def split(self, hand_index):
        split_hand = self.hands[hand_index]
        if split_hand.split_check() == False:
            raise InvalidHandError("Invalid hand to split")
        if self.balance - self.current_bet < 0:
            raise InsufficientFundsError("Insufficient Funds")
        self.balance -= self.current_bet
        

        split_1 = Hand()
        split_2 = Hand()
        split_1.add_card(split_hand.cards[0])
        split_2.add_card(split_hand.cards[1])

        self.hands[hand_index] = split_1
        self.hands.insert(hand_index + 1, split_2)
    
    def insurance_choice(self, choice):
        self.insurance = choice
        # if insurance is taken, check for valid funding and deduct insurance unit from bal
        if choice == True:
            insurance_size = self.current_bet/2
            if self.balance - insurance_size < 0:
                raise InsufficientFundsError("Insufficient Funds")
            self.balance -= insurance_size
    
    def player_reset(self):
        self.hands = []
        self.insurance = False
