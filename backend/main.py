from game.game import Game

def main():
    game_state = True
    game = Game()
    while game_state:
        choice = input("Start game? (y/n): ").lower()
        if choice == "y":
            while (True):
                try:
                    balance = int(input ("Enter starting balance: (integer value): "))
                    break
                except ValueError:
                    print("Enter an integer\n")
            game_state = False
            game.play(True, balance)

        elif choice == "n":
            print("Terminating")
            break
        else:
            print("Select valid choice: (y/n)")

   
if __name__ == "__main__":
    main()