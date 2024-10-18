import pygame
from typing import override
from contracts.screen_interfaces import IPlayScreen
from settings import SCREEN_WIDTH

# Load the arrow image for the projectile
arrow_img = pygame.image.load('img/icons/arrow.png').convert_alpha()

# Projectile class representing an arrow
class Arrow(pygame.sprite.Sprite):
    """
    The Arrow class is a projectile that moves across the screen in a given direction.
    It can collide with obstacles, the player, or enemies, dealing damage when it hits.
    """

    def __init__(self, x, y, direction):
        """
        Initialize the Arrow object.
        :param x: The x-coordinate where the arrow is spawned.
        :param y: The y-coordinate where the arrow is spawned.
        :param direction: The direction in which the arrow moves (1 for right, -1 for left).
        """
        super().__init__()
        self.speed = 10  # Speed of the arrow's movement
        self.image = arrow_img  # Set the arrow image
        self.rect = self.image.get_rect()  # Get the boundary box of the arrow image
        self.rect.center = (x, y)  # Set the initial position of the arrow
        self.direction = direction  # Set the direction the arrow will travel (1 or -1)

    @override
    def update(self, *args, **kwargs):
        """
        Update method called every frame to move the arrow and check for collisions.
        """
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            # Move the arrow horizontally according to its direction and speed, adjusting for screen scroll
            self.rect.x += (self.direction*self.speed) + screen.get_screen_scroll()

            # Check if the arrow has gone off-screen and remove it if it has
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()
        
            # Check for collisions with obstacles (e.g., walls, platforms)
            if pygame.sprite.spritecollide(self, screen.get_obstacle_group(), False):
                # If the arrow hits an obstacle, destroy the arrow
                self.kill()

            # Check for collision with the player
            player = screen.get_player()
            if player.alive and pygame.sprite.collide_rect(player, self):
                # If the arrow hits the player, deal 5 damage and destroy the arrow
                player.health -= 5
                self.kill()
            
            # Check for collisions with enemies
            for enemy in screen.get_enemy_group():
                if enemy.alive and pygame.sprite.collide_rect(enemy, self):
                    # If the arrow hits an enemy, deal 25 damage and destroy the arrow
                    enemy.health -= 25
                    self.kill()