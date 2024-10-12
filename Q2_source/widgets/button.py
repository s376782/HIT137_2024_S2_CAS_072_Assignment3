import pygame 
from typing import override

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, callback):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.callback = callback

    @override
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        pos = pygame.mouse.get_pos() # get mouse position

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.callback()			

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

class StartButton(Button):
    def __init__(self, x, y, callback):
        img = pygame.image.load('img/start_btn.png').convert_alpha()
        super().__init__(x, y, img, callback)

class ExitButton(Button):
    def __init__(self, x, y, callback):
        img = pygame.image.load('img/exit_btn.png').convert_alpha()
        super().__init__(x, y, img, callback)

class RestartButton(Button):
    def __init__(self, x, y, callback):
        img = pygame.image.load('img/restart_btn.png').convert_alpha()
        super().__init__(x, y, img, callback)
