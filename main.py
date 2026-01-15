import pygame 
from main_menu import menu
from gameplay import run_game
import json

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_on": True, "difficulty": 10}


pygame.init()

def main():
    settings = load_settings()
    difficulty = settings["difficulty"]
    while True:
        choice = menu()

        if choice == 'start':
            print("Debug: Start Hit")
            run_game(difficulty)

        elif choice == 'quit':

            pygame.quit()
            return

        elif choice == 'menu':
            menu()

if __name__ == "__main__":
    main()