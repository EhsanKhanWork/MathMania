import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
font = pygame.font.SysFont("Arial", 24)

# 1. Define the box (rect)
box_rect = pygame.Rect(100, 100, 200, 50)

# 2. Render the text surface
text_surface = font.render("Hello World!", True, (255, 255, 255))

# 3. Center the text in the box
text_rect = text_surface.get_rect(center=box_rect.center)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((30, 30, 30))
    
    # Draw the box and then the text
    pygame.draw.rect(screen, (0, 128, 255), box_rect)
    screen.blit(text_surface, text_rect)
    
    pygame.display.flip()
pygame.quit()
