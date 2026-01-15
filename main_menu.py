import pygame
import sys
from gameplay import run_game, load_highscore
from background import init_background, draw_background
from loading import show_loading
import os
import json
import json

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_on": True, "difficulty": 10}

def save_settings(settings):
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
    show_settings = False
    show_how_to_play = False
    show_stats = False

    if music_on:
        pygame.mixer.Sound.play(music_sound)

    highscore = load_highscore()

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

    heli_img, heli_rect, heli_speed = init_background(height)

    class Button:
        def __init__(self, text, y):
            self.text = text
            self.rect = pygame.Rect(width // 2 - 125, y, 250, 75)
            self.color = black
        
        def draw(self, surf):
            pygame.draw.rect(surf, self.color, self.rect, border_radius=12)
            msg = button_font.render(self.text, True, white)
            surf.blit(msg, (self.rect.centerx - msg.get_width() // 2, self.rect.centery - msg.get_height() // 2))

        def hovered(self, mouse):
            return self.rect.collidepoint(mouse)

    def settings_menu():
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(50, 200, width - 100, 450)
        pygame.draw.rect(screen, black, box, border_radius=25)
        pygame.draw.rect(screen, black, box, 2, border_radius=25)

        title = title_font.render("Settings", True, white)
        screen.blit(title, title.get_rect(center=(width // 2, box.y + 60)))
        
        sound_btn = pygame.Rect(box.x + 40, box.y + 120, box.width - 80, 80)
        diff_btn = pygame.Rect(box.x + 40, box.y + 220, box.width - 80, 80)
        back_btn = pygame.Rect(box.x + 40, box.y + 320, box.width - 80, 80)

        mouse_pos = pygame.mouse.get_pos()

        for btn, text in [(sound_btn, f"Sound: {'On' if music_on else 'Off'}"), (diff_btn, f"Difficulty: {difficulty}"), (back_btn, 'Back')]:
            
            pygame.draw.rect(screen, box_color, btn, border_radius=12)
            pygame.draw.rect(screen, box_color, btn, border_radius=12)
            txt = font.render(text, True, black)
            screen.blit(txt, txt.get_rect(center=btn.center))

        return sound_btn, diff_btn, back_btn

    def guide():
        screen.fill(black)

        box = pygame.Rect(50, 100, width - 100, height - 200)
        pygame.draw.rect(screen, black, box, border_radius=25)
        pygame.draw.rect(screen, black, box, 2, border_radius=25)

        title = title_font.render("How to Play", True, white)
        screen.blit(title, title.get_rect(center=(width // 2, box.y + 60)))

        instructions = [
            "1. Solve math problems by jumping on the correct platforms.",
            "2. Use arrow keys to move left and right.",
            "3. Press spacebar to jump.",
            "4. Each correct answer earns you points.",
            "5. Avoid wrong answers to keep playing!",
            "6. Reach higher levels for more challenging problems."
        ]

        for i, line in enumerate(instructions):
            instr_text = small_font.render(line, True, white)
            screen.blit(instr_text, (box.x + 30, box.y + 120 + i * 50))
        
        back_btn = pygame.Rect(box.x + 40, box.y + height - 250, box.width - 80, 50)
        pygame.draw.rect(screen, box_color, back_btn, border_radius=12)
        txt = font.render("Back", True, black)
        screen.blit(txt, txt.get_rect(center=back_btn.center))

        return back_btn
    
    def stats_menu():
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        bx = pygame.Rect(50, 150, width - 100, 500)
        pygame.draw.rect(screen, black, bx, border_radius=25)
        pygame.draw.rect(screen, black, bx, 2, border_radius=25)


        title = title_font.render("Statistics", True, white)
        screen.blit(title, title.get_rect(center=(width // 2, 100)))
        
        stats = [
            f"Highscore: {highscore}",
        ]

        for i, line in enumerate(stats):
            stat_text = small_font.render(line, True, white)
            screen.blit(stat_text, (width // 2 - stat_text.get_width() // 2, 200 + i * 50))
        
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_settings:
                    
                    if back_btn.collidepoint(mouse_pos):
                        show_settings = False
                    elif sound_btn.collidepoint(mouse_pos):
                        if music_on:
                            pygame.mixer.Sound.stop(music_sound)
                            music_on = False
                        else:
                            pygame.mixer.Sound.play(music_sound)
                            music_on = True
                        settings["music_on"] = music_on
                        save_settings(settings)
                    elif diff_btn.collidepoint(mouse_pos):
                        difficulties = [5, 10, 15, 20]
                        current_index = difficulties.index(difficulty)
                        difficulty = difficulties[(current_index + 1) % len(difficulties)]
                        settings["difficulty"] = difficulty
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

