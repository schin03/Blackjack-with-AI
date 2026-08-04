from .shoe import Shoe
from .hand import Hand

class Game:
    def play(self, state, bal):
        shoe = Shoe()
        game_start = state
        self.balance = bal
        while (game_start):
            self.bust_state = False
            self.blackjack = False
            self.bet_size = 0
            self.handle_bet()
            print("Dealing hand... \n")
            player_hand = Hand()
            dealer_hand = Hand()
            valid_game = True
            self.deal_start(player_hand, dealer_hand, shoe)
            if self.blackjack == False:
                while (valid_game):
                    self.show_state(player_hand, dealer_hand)
                    valid_game = self.handle_hit(player_hand, shoe)
            
            self.handle_dealer(dealer_hand, shoe)
            self.show_result(player_hand, dealer_hand)
            print("\nCards in shoe left: ", shoe.cards_left())

            game_start = self.handle_redeal()

    def handle_bet(self):
        while (True):
            print("\nCurrent balance: ", self.balance)
            try:
                bet = int(input("Enter bet amount: "))
                if bet > self.balance:
                    print("Choose a valid betting amount.")
                else:
                    break
            except ValueError:
                print("Enter an integer.")
        self.bet_size = bet
        self.balance -= bet

    def deal_start(self, player, dealer, shoe):
        player.add_card(shoe.deal())
        dealer.add_card(shoe.deal())
        player.add_card(shoe.deal())
        hidden_card = shoe.deal()
        hidden_card.set_hidden(True)
        dealer.add_card(hidden_card)
        if player.get_value() == 21:
            self.blackjack = True
    
    def handle_hit(self, player, shoe):
        choice = input("Hit? (y/n): ").lower()
        while True:
            if choice == "y":
                self.hit(player, shoe)
                break
            elif choice == "n":
                return False
            else:
                print("Select valid choice: (y/n)")
        if player.get_value() >= 21:
            self.bust_state = True
            return False
        return True

    def hit(self, hand, shoe):
        hand.add_card(shoe.deal())

    def handle_dealer(self, dealer, shoe):
        dealer.reveal_last()
        if self.bust_state or self.blackjack:
            return
        while True:
            if dealer.get_value() < 17:
                self.hit(dealer, shoe)
            else:
                break
        

    def show_state(self, player, dealer):
        print("\nPlayer Cards: ", player)
        print(player.get_value())
        print("Dealer cards: ", dealer)
        print(dealer.get_value())

    def show_result(self, player, dealer):
        self.show_state(player, dealer)
        if self.blackjack:
            winnings = self.bet_size * 1.5 + self.bet_size
            self.balance += winnings
            print("Player Win. Player Blackjack")
        elif self.bust_state:
            print("Dealer Win. Player Bust")
            return
        elif dealer.get_value() > 21:
            print("Player Win. Dealer Bust")
            self.balance += 2 * self.bet_size
        else:
            if player.get_value() > dealer.get_value():
                print("Player Win.")
                self.balance += 2 * self.bet_size
            elif player.get_value() == dealer.get_value():
                print("Player Tie. Push")
                self.balance += self.bet_size
            else:
                print("Dealer Win.")
                return

    
    def handle_redeal(self):
        choice = input("Redeal? (y/n): ").lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Select valid choice: (y/n)")