import os
import pygame

from game import Game
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

game = Game()

while game.running:
    clock.tick(FPS)

    game.handle_events(pygame.event.get())
    game.update()
    game.draw(screen)

    pygame.display.update()

pygame.quit()