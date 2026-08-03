from .shoe import Shoe
from .hand import Hand

class Game:
    def play(self, state):
        shoe = Shoe()
        game_start = state
        while (game_start):
            print("Dealing hand... \n")
            player_hand = Hand()
            dealer_hand = Hand()
            valid_game = True
            self.deal_start(player_hand, dealer_hand, shoe)
            while (valid_game):
                self.show_state(player_hand, dealer_hand)
                valid_game = self.handle_hit(player_hand, shoe)
            
            self.handle_dealer(dealer_hand, shoe)
            self.show_result(player_hand, dealer_hand)
            print("\nCards in shoe left: ", shoe.cards_left())

            game_start = self.handle_redeal()

    def deal_start(self, player, dealer, shoe):
        player.add_card(shoe.deal())
        dealer.add_card(shoe.deal())
        player.add_card(shoe.deal())
        hidden_card = shoe.deal()
        hidden_card.set_hidden(True)
        dealer.add_card(hidden_card)
    
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
            return False
        return True

    def hit(self, hand, shoe):
        hand.add_card(shoe.deal())

    def handle_dealer(self, dealer, shoe):
        dealer.reveal_last()
        valid_hand = True
        while valid_hand:
            if dealer.get_value() >= 17:
                valid_hand = False
            else:
                self.hit(dealer, shoe)
        

    def show_state(self, player, dealer):
        print("\nPlayer Cards: ", player)
        print(player.get_value())
        print("Dealer cards: ", dealer)
        print(dealer.get_value())

    def show_result(self, player, dealer):
        self.show_state(player, dealer)
    
    def handle_redeal(self):
        choice = input("Redeal? (y/n): ").lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Select valid choice: (y/n)")