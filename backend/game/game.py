from .shoe import Shoe
from .hand import Hand

class Game:
    def play(self, state):
        shoe = Shoe()
        gameStart = state
        if (gameStart):
            player_hand = Hand()
            dealer_hand = Hand()
            valid_game = True
            self.deal_start(player_hand, dealer_hand, shoe)
            print("Player Cards: ", player_hand)
            print(player_hand.get_value())
            print("Dealer cards: ", dealer_hand)
            print(dealer_hand.get_value())

            while (valid_game):
                choice = handle_hit()
                
            print("\nCards in shoe left: ", shoe.cards_left())


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
                return True
            elif choice == "n":
                return False
            else:
                print("Select valid choice: (y/n)")
    def hit(self, player, shoe):
        player.add_card(shoe.deal())

