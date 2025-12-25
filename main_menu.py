import pygame
import sys
from gameplay import run_game
from test import init_background, draw_background

pygame.init()

def menu():
    # Set window dimensions
    width = 600
    height = 800

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption('Math Mania')

    black = (0, 0, 0)
    white = (255, 255, 255)
    grid_color = (180, 200, 220)

    title_font = pygame.font.SysFont('arialblack', 60)
    button_font = pygame.font.SysFont('arial', 26)

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


    buttons = [ 
        Button("Start", 420),
        Button("Leaderboard", 520),
        Button("Quit", 620)
    ]

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)
        draw_background(screen, heli_img, heli_rect, heli_speed, width)
        
        mouse_pos = pygame.mouse.get_pos()

        title1 = title_font.render('Math', True, black)
        title2 = title_font.render('Mania', True, black)

        screen.blit(pygame.transform.rotate(title1, -15), (30, 40))
        screen.blit(pygame.transform.rotate(title2, -10), (60, 140))

        for button in buttons:
            if button.is_hovered(mouse_pos):
                button.color = (40, 40, 40)
            else:
                button.color = black
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_hovered(mouse_pos):
                        
                        if button.text == 'Start':
                            return "start"
                            
                        
                        elif button.text == 'Leaderboard':
                            print("Leaderboard Clicked")

                        elif button.text == 'Quit':
                            return "quit"

        pygame.display.update()

