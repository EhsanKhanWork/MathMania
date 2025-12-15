import pygame
import sys

from gameplay import new_run_game

pygame.init()

def menu():
    # Set window dimensions
    width = 600
    height = 800

    

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Math Mania')

    black = (0, 0, 0)
    white = (255, 255, 255)
    grid_color = (180, 200, 220)

    title_font = pygame.font.SysFont('arialblack', 60)
    button_font = pygame.font.SysFont('arial', 26)

    class Button:
        def __init__(self, text, y):
            self.text = text
            self.rect = pygame.Rect(width // 2 - 100, y, 200, 55)
            self.color = black
        
        def draw(self, surf):
            pygame.draw.rect(surf, self.color, self.rect, border_radius=12)
            msg = button_font.render(self.text, True, white)
            surf.blit(msg, (self.rect.centerx - msg.get_width() // 2, self.rect.centery - msg.get_height() // 2))

        def is_hovered(self, mouse):
            return self.rect.collidepoint(mouse)


    buttons = [ 
        Button("Start", 300),
        Button("Leaderboard", 380),
        Button("Quit", 460)
    ]

    running = True
    while running:
        screen.fill(white)
        
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

