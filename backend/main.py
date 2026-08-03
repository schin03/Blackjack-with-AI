from game.game import Game

def main():
    while True:
        choice = input("Start game? (y/n): ").lower()
        if choice == "y":
            print("Dealing hand... \n")
            game = Game()
            game.play(True)

        elif choice == "n":
            print("Terminating")
            break
        else:
            print("Select valid choice: (y/n)")

   
if __name__ == "__main__":
    main()