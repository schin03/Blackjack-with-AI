from game.game import Game

def main():
    game_state = True
    game = Game()
    while game_state:
        choice = input("Start game? (y/n): ").lower()
        if choice == "y":
            game_state = False
            game.play(True)

        elif choice == "n":
            print("Terminating")
            break
        else:
            print("Select valid choice: (y/n)")

   
if __name__ == "__main__":
    main()