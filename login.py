import pygame
import sys
import json
import os

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)
    
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)
  

class TextInput:
    #text input box for username and password entry
    def __init__(self, x, y, width, height, font, placeholder=""):
        # defines the input box properties, stores text 
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)
        self.text = ""
        self.font = font
        self.placeholder = placeholder
        # indicator for active input box
        self.active = False

    def handle_event(self, event):
        #Handles events related to the text input box
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1] # Removes last character
            else:
                self.text += event.unicode

    def draw(self, screen):
        #Draws the text input box on the screen
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt = self.text 
        if self.text: 
            txt = self.text
        else:
            txt = self.placeholder
        text_surf = self.font.render(txt, True, (255, 255, 255))
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

def login_screen():
    pygame.init()
    width, height = 600, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Math Mania - Login')


    font = pygame.font.Font(os.path.join('assets/game.ttf'), 30)
    button_font = pygame.font.Font(os.path.join('assets/game.ttf'), 26)

    users = load_users()

    mode = "signin"  # or "signup"

    username_input = TextInput(width//2 - 100, 300, 200, 40, font, "Username")
    password_input = TextInput(width//2 - 100, 360, 200, 40, font, "Password")

    # password masking didnt work well with current setup so leaving as is for now

    signin_btn = pygame.Rect(width//2 - 100, 420, 200, 50)
    switch_btn = pygame.Rect(width//2 - 100, 540, 250, 50)

    message = ""

    clock = pygame.time.Clock()
    clock.tick(60)

    running = True
    while running:
        screen.fill((135, 206, 235))

        title = font.render("Math Mania", True, (255, 255, 255))
        screen.blit(title, (width//2 - title.get_width()//2, 200))

        username_input.draw(screen)
        password_input.draw(screen)

        pygame.draw.rect(screen, (255, 255, 255), signin_btn, 2)
        signin_text = button_font.render("Sign In" if mode == "signin" else "Sign Up", True, (255, 255, 255))
        screen.blit(signin_text, (signin_btn.centerx - signin_text.get_width()//2, signin_btn.centery - signin_text.get_height()//2))

        pygame.draw.rect(screen, (255, 255, 255), switch_btn, 2)
        switch_text = button_font.render("Switch to Sign Up" if mode == "signin" else "Switch to Sign In", True, (255, 255, 255))
        screen.blit(switch_text, (switch_btn.centerx - switch_text.get_width()//2, switch_btn.centery - switch_text.get_height()//2))

        if message:
            msg_surf = font.render(message, True, (255, 0, 0))
            screen.blit(msg_surf, (width//2 - msg_surf.get_width()//2, 600))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            username_input.handle_event(event)
            password_input.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if signin_btn.collidepoint(event.pos):
                    # Check if the sign in/sign up button was clicked
                    username = username_input.text
                    password = password_input.text
                    # Retrieving username and password
                    if mode == "signin":
                        # Validating user credentials
                        if username in users and users[username] == password:
                            return username  
                        else:
                            message = "Invalid username or password"
                    else:  # Sign up mode
                        if username in users:
                            message = "Username already exists"
                        elif not username or not password:
                            message = "Enter username and password"
                        else:
                            users[username] = password
                            save_users(users) # Save new user data
                            message = "Account created!"
                            mode = "signin"
                elif switch_btn.collidepoint(event.pos):
                    # swapping between signin and signup modes
                    mode = "signup" if mode == "signin" else "signin"
                    message = ""

    return None
