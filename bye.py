# Imports
import pygame, sys, threading, os

pygame.init()


def show_bye(screen, width, height):
	
    bye = pygame.mixer.Sound(os.path.join('assets/bye.mp3'))

    pygame.mixer.Sound.play(bye)
    pygame.mixer.Sound.stop(bye)

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 28)

    screen.fill((0, 0, 0))

    title = font.render("Math Mania", True, (255, 255, 255))
    loading = small_font.render("Bye Bye", True, (200, 200, 200))

    screen.blit(title, title.get_rect(center=(width // 2, height // 2 - 40)))
    screen.blit(loading, loading.get_rect(center=(width // 2, height // 2 + 20)))


    pygame.display.flip()

