import pygame
from typing import override
from contracts.screen_interfaces import IScrollScreen

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    @override
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IScrollScreen):
            #scroll
            self.rect.x += screen.get_screen_scroll()

            EXPLOSION_SPEED = 4
            #update explosion amimation
            self.counter += 1

            if self.counter >= EXPLOSION_SPEED:
                self.counter = 0
                self.frame_index += 1
                #if the animation is complete then delete the explosion
                if self.frame_index >= len(self.images):
                    self.kill()
                else:
                    self.image = self.images[self.frame_index]