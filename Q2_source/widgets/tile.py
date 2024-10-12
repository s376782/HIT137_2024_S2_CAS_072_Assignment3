import pygame
from typing import override
from contracts.screen_interfaces import IScrollScreen
from settings import TILE_SIZE, TILE_TYPES

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y):
        super().__init__()
        self.image = img_list[tile]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    @override
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IScrollScreen):
            self.rect.x += screen.get_screen_scroll()