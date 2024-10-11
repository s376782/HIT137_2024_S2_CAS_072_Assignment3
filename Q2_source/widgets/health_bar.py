from typing import Any, override
import pygame

from contracts.screen_interfaces import IPlayerScreen
from settings import BLACK, GREEN, MAX_HEALTH, RED, SCREEN_HEIGHT, SCREEN_WIDTH

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = 0
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:
        screen: IPlayerScreen = args[0]
        if screen and screen.get_player() and self.health != screen.get_player().health:
            self.health = screen.get_player().health
            ratio = self.health / MAX_HEALTH

            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
            self.rect = self.image.get_rect()
            pygame.draw.rect(self.image, BLACK, (self.x - 2, self.y - 2, 154, 24))
            pygame.draw.rect(self.image, RED, (self.x, self.y, 150, 20))
            pygame.draw.rect(self.image, GREEN, (self.x, self.y, 150 * ratio, 20))