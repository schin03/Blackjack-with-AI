from .shoe import Shoe
from .hand import Hand

class Game:
    def play(self):
        shoe = Shoe()
        player_hand = Hand()
        dealer_hand = Hand()

        self.deal_start(player_hand, dealer_hand, shoe)


        print("Player Cards: ", player_hand)
        print("\n", player_hand.get_value())
        print("\nDealer cards: ", dealer_hand)
        print("\n", dealer_hand.get_value())


    def deal_start(self, player, dealer, shoe):
        player.add_card(shoe.deal())
        dealer.add_card(shoe.deal())
        player.add_card(shoe.deal())
        dealer.add_card(shoe.deal())

