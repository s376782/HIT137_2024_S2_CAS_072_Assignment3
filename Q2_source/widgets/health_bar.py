import pygame
from typing import override
from contracts.screen_interfaces import IPlayScreen
from settings import BLACK, GREEN, MAX_HEALTH, RED, SCREEN_HEIGHT, SCREEN_WIDTH


# Create Health bar
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.update_image(0)

    def update_image(self, health):
        self.health = health
        ratio = self.health / MAX_HEALTH

        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(self.image, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(self.image, GREEN, (self.x, self.y, 150 * ratio, 20))        

    @override
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            player = screen.get_player()
            if player and self.health != player.health:
                self.update_image(player.health)