import pygame
import sys
from gameplay import run_game
from background import init_background, draw_background
from loading import show_loading
import os

pygame.init()

def menu():
    width = 600
    height = 800

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Math Mania')

    music_sound = pygame.mixer.Sound(os.path.join("assets/music.mp3"))
    pygame.mixer.Sound.play(music_sound)

    bombo_sound = pygame.mixer.Sound(os.path.join("assets/bombo.mp3"))

    show_loading(screen, width, height)
    pygame.time.delay(2000)

    music_on = True
    show_settings = False

    black = (0, 0, 0)
    white = (255, 255, 255)
    grid_color = (180, 200, 220)
    box_color = white

    setting_button = pygame.image.load(os.path.join('assets/setting.png'))
    setting_button = pygame.transform.scale(setting_button, (50, 50))

    setting_rect = setting_button.get_rect()
    setting_rect.top = 10
    setting_rect.right = width - 10

    title_font = pygame.font.SysFont('arialblack', 60)
    button_font = pygame.font.SysFont('arial', 26)
    font = pygame.font.Font(None, 50)

    heli_img, heli_rect, heli_speed = init_background(height)

    class Button:
        def __init__(self, text, y):
            self.text = text
            self.rect = pygame.Rect(width // 2 - 150, y, 300, 80)
            self.color = black
        
        def draw(self, surf):
            pygame.draw.rect(surf, self.color, self.rect, border_radius=12)
            msg = button_font.render(self.text, True, white)
            surf.blit(msg, (self.rect.centerx - msg.get_width() // 2, self.rect.centery - msg.get_height() // 2))

        def is_hovered(self, mouse):
            return self.rect.collidepoint(mouse)

    def settings_menu():
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(50, 200, width - 100, 300)
        pygame.draw.rect(screen, black, box, border_radius=25)
        pygame.draw.rect(screen, black, box, 2, border_radius=25)

        title = title_font.render("Settings", True, black)
        screen.blit(title, title.get_rect(center=(width // 2, box.y + 60)))
        
        sound_btn = pygame.Rect(box.x + 40, box.y + 140, box.width - 80, 50)
        back_btn = pygame.Rect(box.x + 40, box.y + 210, box.width - 80, 50)

        mouse_pos = pygame.mouse.get_pos()

        for btn, text in [(sound_btn, "Sound", ), (back_btn, 'Back')]:
            pygame.draw.rect(screen, box_color, btn, border_radius=12)
            pygame.draw.rect(screen, box_color, btn, border_radius=12)
            txt = font.render(text, True, black)
            screen.blit(txt, txt.get_rect(center=btn.center))

        return sound_btn, back_btn

    buttons = [ 
        Button("Start", 420),
        Button("Leaderboard", 520),
        Button("Quit", 620)
    ]

    clock = pygame.time.Clock()

    sound_btn = pygame.Rect(0, 0, 0, 0)
    back_btn = pygame.Rect(0, 0, 0, 0)

    running = True
    while running:
        clock.tick(60)
        draw_background(screen, heli_img, heli_rect, heli_speed, width)
       
        mouse_pos = pygame.mouse.get_pos()

        title1 = title_font.render('Math', True, black)
        title2 = title_font.render('Mania', True, black)

        screen.blit(pygame.transform.rotate(title1, -15), (30, 40))
        screen.blit(pygame.transform.rotate(title2, -10), (60, 140))
        screen.blit(setting_button, setting_rect)

        for button in buttons:
            if button.is_hovered(mouse_pos):
                button.color = (40, 40, 40)
            else:
                button.color = black
            button.draw(screen)

        if show_settings:
            sound_btn, back_btn = settings_menu()

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
            
                elif setting_rect.collidepoint(mouse_pos):
                    show_settings = True
                
                else:
                    for button in buttons:
                        if button.is_hovered(mouse_pos):
                        
                            if button.text == 'Start':
                                pygame.mixer.Sound.stop(music_sound)
                                return "start"
                        
                            elif button.text == 'Leaderboard':
                                print("Leaderboard Clicked")

                            elif button.text == 'Quit':
                                return "quit"

        pygame.display.update()

