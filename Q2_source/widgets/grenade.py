import pygame
from typing import override
from widgets.explosion import Explosion
from contracts.screen_interfaces import IPlayScreen
from settings import GRAVITY, TILE_SIZE

grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.05)

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    @override
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            self.vel_y += GRAVITY
            dx = self.direction * self.speed
            dy = self.vel_y

            #check for collision with level
            for tile in screen.get_obstacle_group():
                #check collision with walls
                if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = self.direction * self.speed
                #check for collision in the y direction
                if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.speed = 0
                    #check if below the ground, i.e. thrown up
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom

            #update grenade position
            self.rect.x += dx + screen.get_screen_scroll()
            self.rect.y += dy

            #countdown timer
            self.timer -= 1
            if self.timer <= 0:
                self.kill()
                grenade_fx.play()
                explosion = Explosion(self.rect.x, self.rect.y, 0.5)
                screen.explosion_group.add(explosion)
                #do damage to anyone that is nearby
                if abs(self.rect.centerx - screen.get_player().rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - screen.get_player().rect.centery) < TILE_SIZE * 2:
                    screen.get_player().health -= 50
                for enemy in screen.get_enemy_group():
                    if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 50