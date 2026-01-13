import pygame
import os

def init_background(height):
    heli_img = pygame.image.load(
        os.path.join("assets", "helicopter.png")).convert_alpha()
    heli_img = pygame.transform.scale(heli_img, (300, 300))

    heli_rect = heli_img.get_rect(midleft=(-heli_img.get_width(), height // 2))
    speed = 6

    return heli_img, heli_rect, speed

def draw_background(screen, heli_img, heli_rect, speed, width):
    heli_rect.x += speed
    if heli_rect.left > width:
        heli_rect.right = 0

    screen.fill((135, 206, 235))
    screen.blit(heli_img, heli_rect)


 
