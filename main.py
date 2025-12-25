import pygame 
from main_menu import menu
from gameplay import run_game

pygame.init()

def main():
    while True:
        choice = menu()

        if choice == 'start':
            print("Debug: Start Hit")
            run_game()

        elif choice == 'quit':
            pygame.quit()
            return

if __name__ == "__main__":
    main()