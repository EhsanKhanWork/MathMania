import pygame 
from main_menu import menu
from gameplay import run_game
from login import login_screen
import json

def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)
    

pygame.init()

def main(): # Main control function for the program
    user = login_screen()
    if user is None:
        return  # if login failed, exit
    settings = load_settings()
    difficulty = settings["difficulty"]
    while True:
        # the main menu loop that handles user choices
        choice = menu()

        if choice == 'start':
            run_game(difficulty)

        elif choice == 'quit':

            pygame.quit()
            return

        elif choice == 'menu':
            menu() # redisplay menu again

if __name__ == "__main__":
    main()