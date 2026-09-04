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
        hand = self.hands[hand_index]

        if self.balance - hand.bet < 0:
            raise InsufficientFundsError("Insufficient Funds")
        if len(hand) != 2:
            raise InvalidHandError("Invalid hand to double")

        self.player.balance -= hand.bet
        hand.bet *= 2
    
        self.hit(hand_index, shoe)
    
    def split(self, hand_index):
        og_hand = self.hands[hand_index]

        if not og_hand.can_split():
            raise InvalidHandError("Invalid hand to split")
        if self.balance < og_hand.bet:
            raise InsufficientFundsError("Insufficient Funds")

        self.balance -= self.og_hand.bet

        left = Hand(bet = og_hand.bet, is_split = True)
        right = Hand(bet = og_hand.bet, is_split = True)

        left.add_card(og_hand.cards[0])
        right.add_card(og_hand.cards[1])

        self.hands[hand_index] = left
        self.hands.insert(hand_index + 1, right)
    
    def insurance_choice(self, choice):
        self.insurance = choice
        hand = self.hands[0]
        # if insurance is taken, check for valid funding and deduct insurance unit from bal
        if choice == True:
            insurance_size = hand.bet/2
            if self.balance - insurance_size < 0:
                raise InsufficientFundsError("Insufficient Funds")
            self.balance -= insurance_size
    
    def player_reset(self):
        self.hands = []
        self.insurance = False
