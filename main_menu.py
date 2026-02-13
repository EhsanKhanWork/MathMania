import pygame
import sys
from gameplay import run_game, load_highscore, load_time
from background import init_background, draw_background
from loading import show_loading
import os
import json


def load_settings():
    #Load settings from a JSON file.
    #Returns a dictionary with settings
    with open("settings.json", "r") as f:
        return json.load(f)
    

def save_settings(settings):
    #Save settings to a JSON file.
    with open("settings.json", "w") as f:
        json.dump(settings, f)


pygame.init()

def menu():
    width = 600
    height = 800

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Math Mania')

    music_sound = pygame.mixer.Sound(os.path.join("assets/music.mp3"))

    bombo_sound = pygame.mixer.Sound(os.path.join("assets/bombo.mp3"))

    show_loading(screen, width, height)
    pygame.time.delay(2000)

    settings = load_settings()
    music_on = settings["music_on"]
    difficulty = settings["difficulty"]

    # menu state flags 
    # tells the game what to display 
    show_settings = False
    show_how_to_play = False
    show_stats = False

    if music_on:
        pygame.mixer.Sound.play(music_sound)

    highscore = load_highscore()
    time = load_time()

    black = (0, 0, 0)
    white = (255, 255, 255)
    grid_color = (180, 200, 220)
    box_color = white
    hover_color = (200, 200, 200)

    game_font = os.path.join('assets/game.ttf')

    title_font = pygame.font.Font(game_font, 60)
    button_font = pygame.font.Font(game_font, 26)
    font = pygame.font.Font(game_font, 50)
    small_font = pygame.font.Font(game_font, 20)
    # i duplicated fonts because of scope issues

    highscore_text = font.render(f'Highscore: {highscore}', True, black)

    setting_button = pygame.image.load(os.path.join('assets/setting.png'))
    setting_button = pygame.transform.scale(setting_button, (50, 50))

    setting_rect = setting_button.get_rect()
    setting_rect.top = 10
    setting_rect.right = width - 10

    score_x = width // 2 - highscore_text.get_width() // 2
    score_y = 220

    game_font = os.path.join('assets/game.ttf')

    title_font = pygame.font.Font(game_font, 60)
    button_font = pygame.font.Font(game_font, 26)
    font = pygame.font.Font(game_font, 50)
    small_font = pygame.font.Font(game_font, 26)
    list_font = pygame.font.Font(game_font, 18)
    #same here

    heli_img, heli_rect, heli_speed = init_background(height)

    class Button:
        # Represents a clickable button in the menu.
        def __init__(self, text, y):
            # Initialize button properties 
            self.text = text
            self.rect = pygame.Rect(width // 2 - 125, y, 250, 75)
            self.color = black
        
        def draw(self, surf):
            # Draws the button on the given surface
            pygame.draw.rect(surf, self.color, self.rect, border_radius=12)
            msg = button_font.render(self.text, True, white)
            surf.blit(msg, (self.rect.centerx - msg.get_width() // 2, self.rect.centery - msg.get_height() // 2))

        def hovered(self, mouse):
            return self.rect.collidepoint(mouse)

    def settings_menu():
        
        #Displays the settings menu.
        #Returns the rectangles for the sound, difficulty, and back buttons.
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # Main settings box is drawn
        box = pygame.Rect(50, 200, width - 100, 450)
        pygame.draw.rect(screen, black, box, border_radius=25)
        pygame.draw.rect(screen, black, box, 2, border_radius=25)
        # Rendering title of settings menu
        title = title_font.render("Settings", True, white)
        screen.blit(title, title.get_rect(center=(width // 2, box.y + 60)))
        # Defining clickable button areas for each setting option
        sound_btn = pygame.Rect(box.x + 40, box.y + 120, box.width - 80, 80)
        diff_btn = pygame.Rect(box.x + 40, box.y + 220, box.width - 80, 80)
        back_btn = pygame.Rect(box.x + 40, box.y + 320, box.width - 80, 80)

        mouse_pos = pygame.mouse.get_pos()

        for btn, text in [
            (sound_btn, f"Sound: {'On' if music_on else 'Off'}"), 
            (diff_btn, f"Difficulty: {difficulty}"), (back_btn, 'Back')]:
            
            pygame.draw.rect(screen, box_color, btn, border_radius=12)
            pygame.draw.rect(screen, box_color, btn, border_radius=12)
            txt = font.render(text, True, black)
            screen.blit(txt, txt.get_rect(center=btn.center))

        return sound_btn, diff_btn, back_btn

    def guide():
        
        # Displays the 'How to Play' guide.
    
        screen.fill(black)

        # Draw main guide box
        box = pygame.Rect(50, 100, width - 100, height - 200)
        pygame.draw.rect(screen, black, box, border_radius=25)
        pygame.draw.rect(screen, black, box, 2, border_radius=25)

        title = title_font.render("How to Play", True, white)
        screen.blit(title, title.get_rect(center=(width // 2, box.y + 60)))
        # Displaying instructions
        instructions = [
            "1. Solve math problems by jumping" 
            " on the correct platform.",
            "2. Use arrow keys to move left and right.",
            "3. Press spacebar to jump.",
            "4. Each correct answer earns you points.",
            "5. Avoid wrong answers to keep playing!",
            "6. Reach higher levels for more challenging problems."
        ]
        # Render each instruction line vertically
        for i, line in enumerate(instructions):
            instr_text = list_font.render(line, True, white)
            screen.blit(instr_text, (box.x - 25, box.y + 120 + i * 50))
        
        # Draw a back button to exit guide
        back_btn = pygame.Rect(box.x + 40, box.y + height - 250, box.width - 80, 50)
        pygame.draw.rect(screen, box_color, back_btn, border_radius=12)
        txt = font.render("Back", True, black)
        screen.blit(txt, txt.get_rect(center=back_btn.center))

        return back_btn
    
    def stats_menu():
        '''
        Displays the statistics menu.
        Shows highscore and longest time survived
        '''
        # Created a semi transparent overlay for dimmed background
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        # Main statistics box
        bx = pygame.Rect(50, 150, width - 100, 500)
        pygame.draw.rect(screen, black, bx, border_radius=25)
        pygame.draw.rect(screen, black, bx, 2, border_radius=25)


        title = title_font.render("Statistics", True, white)
        screen.blit(title, title.get_rect(center=(width // 2, 100)))
        
        stats = [
            f"Highscore: {highscore}",
            f"Longest Time: {time}",
        ]
        # Render each statistic line vertically and centered
        for i, line in enumerate(stats):
            stat_text = small_font.render(line, True, white)
            screen.blit(stat_text, (width // 2 - stat_text.get_width() // 2, 200 + i * 50))
        # Draw exit button to close statistics menu
        exit_btn = pygame.Rect(bx.x + 40, bx.y + 400, bx.width - 80, 50)
        pygame.draw.rect(screen, box_color, exit_btn, border_radius=12)
        txt = font.render("Exit", True, black)
        screen.blit(txt, txt.get_rect(center=exit_btn.center))

        return exit_btn

    buttons = [ 
        Button("Start", 420),
        Button("How to Play", 500),
        Button("Statistics", 580),
        Button("Quit", 660)
    ]

    clock = pygame.time.Clock()

    sound_btn = pygame.Rect(0, 0, 0, 0)
    diff_btn = pygame.Rect(0, 0, 0, 0)
    back_btn = pygame.Rect(0, 0, 0, 0)

    running = True
    while running:
        clock.tick(60)
        draw_background(screen, heli_img, heli_rect, heli_speed, width)
       
        mouse_pos = pygame.mouse.get_pos()

        title1 = title_font.render('Math', True, black)
        title2 = title_font.render('Mania', True, black)

        screen.blit(title1, title1.get_rect(center=(width // 2, 60)))
        screen.blit(title2, title2.get_rect(center=(width // 2, 140)))
        
        score_box = pygame.Rect(score_x - 20, score_y - 10, highscore_text.get_width() + 40, highscore_text.get_height() + 20)
        pygame.draw.rect(screen, box_color, score_box, border_radius=12)
        screen.blit(highscore_text, (score_x, score_y))
        
        screen.blit(setting_button, setting_rect)

        for button in buttons:
            # for each button, check if hovered and change color accordingly
            # not needing to repeat draw code over and over again
            if button.hovered(mouse_pos):
                button.color = (40, 40, 40)
            else:
                button.color = black
            button.draw(screen)

        if show_settings:
            sound_btn, diff_btn, back_btn = settings_menu()

        if show_how_to_play:
            back_btn = guide()

        if show_stats:
            exit_btn = stats_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handling mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_settings: # Only if the settings are being shown
                    if back_btn.collidepoint(mouse_pos):
                        show_settings = False # Exit settings menu
                    elif sound_btn.collidepoint(mouse_pos):
                        if music_on: 
                            # Toggle music off
                            pygame.mixer.Sound.stop(music_sound)
                            music_on = False
                        else:
                            # Toggle music on
                            pygame.mixer.Sound.play(music_sound)
                            music_on = True
                        settings["music_on"] = music_on
                        save_settings(settings)
                        # Saving updated music setting (refer to the top function)
                    elif diff_btn.collidepoint(mouse_pos):
                        # Cycle through predefined difficulty levels
                        difficulties = [5, 10, 15, 20] # List of difficulties 
                        current_index = difficulties.index(difficulty)
                        # Get current difficulty index
                        difficulty = difficulties[(current_index + 1) % len(difficulties)]
                        settings["difficulty"] = difficulty
                        # Save the updated difficulty setting
                        save_settings(settings)
            
                elif setting_rect.collidepoint(mouse_pos):
                    show_settings = True
                
                elif show_how_to_play:
                    if back_btn.collidepoint(mouse_pos):
                        show_how_to_play = False
                
                elif show_stats:
                    if exit_btn.collidepoint(mouse_pos):
                        show_stats = False

                else:
                    # This block is kind of self explanatory
                    # But it uses a for loop to apply the logic to all buttons
                    for button in buttons:
                        if button.hovered(mouse_pos):
                        
                            if button.text == 'Start':
                                pygame.mixer.Sound.stop(music_sound)
                                return "start"
                        
                            elif button.text == 'How to Play':
                                show_how_to_play = True
                            
                            elif button.text == 'Statistics':
                                show_stats = True

                            elif button.text == 'Quit':
                                return "quit"

        pygame.display.update()

