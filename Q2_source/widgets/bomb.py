import pygame
from typing import override
from widgets.explosion import Explosion
from contracts.screen_interfaces import IPlayScreen
from settings import GRAVITY, TILE_SIZE

# Load the bomb image and sound effects
bomb_img = pygame.image.load('img/icons/bomb.png').convert_alpha()
bomb_fx = pygame.mixer.Sound('audio/bomb.wav')
bomb_fx.set_volume(0.05)

# Bomb class representing a thrown explosive
class Bomb(pygame.sprite.Sprite):
    """
    The Bomb class represents a throwable bomb that explodes after a countdown.
    The bomb bounces off obstacles and deals damage to nearby players and enemies upon explosion.
    """

    def __init__(self, x, y, direction):
        """
        Initialize the Bomb object.
        :param x: The x-coordinate where the bomb is thrown.
        :param y: The y-coordinate where the bomb is thrown.
        :param direction: The direction in which the bomb is thrown (1 for right, -1 for left).
        """
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100  # Countdown timer before the bomb explodes
        self.vel_y = -11  # Initial vertical velocity to simulate a throw
        self.speed = 7  # Horizontal speed of the bomb
        self.image = bomb_img  # Set the bomb image
        self.rect = self.image.get_rect()  # Get the boundary box for the bomb image
        self.rect.center = (x, y)  # Set the initial position of the bomb
        self.width = self.image.get_width()  # Store the bomb image width for collision detection
        self.height = self.image.get_height()  # Store the bomb image height for collision detection
        self.direction = direction  # Set the direction of the bomb (-1 for left, 1 for right)

    @override
    def update(self, *args, **kwargs):
        """
        Update the Bomb object's position and handle collisions, countdown, and explosion logic.
        """
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            # Apply gravity to the bomb's vertical velocity
            self.vel_y += GRAVITY
            dx = self.direction * self.speed  # Horizontal movement based on direction
            dy = self.vel_y  # Vertical movement based on gravity

            # Check for collisions with obstacles
            for tile in screen.get_obstacle_group():
                # Check for horizontal collisions (left and right movement)
                new_rect_x = pygame.Rect(self.rect.x + dx, self.rect.y, self.width, self.height)
                if tile.rect.colliderect(new_rect_x):
                    self.direction *= -1  # Reverse direction if it hits a wall
                    dx = self.direction * self.speed  # Adjust horizontal movement after bounce

                # Check for vertical collisions (falling or bouncing)
                new_rect_y = pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)
                if tile.rect.colliderect(new_rect_y):
                    self.speed = 0  # Stop horizontal movement upon collision
                    # Check if the bomb is below the ground (bouncing up)
                    if self.vel_y < 0:
                        self.vel_y = 0  # Stop upward movement
                        dy = tile.rect.bottom - self.rect.top  # Correct position after bounce
                    # Check if the bomb is above the ground (falling)
                    elif self.vel_y >= 0:
                        self.vel_y = 0  # Stop downward movement
                        dy = tile.rect.top - self.rect.bottom  # Correct position after collision

            # Update bomb position with screen scrolling
            self.rect.x += dx + screen.get_screen_scroll()
            self.rect.y += dy

            # Countdown timer for the bomb explosion
            self.timer -= 1
            if self.timer <= 0:
                # Trigger bomb explosion when timer reaches zero
                self.kill()  # Remove the bomb sprite from the game
                bomb_fx.play()  # Play the bomb explosion sound
                explosion = Explosion(self.rect.x, self.rect.y, 0.5)  # Create an explosion effect
                screen.explosion_group.add(explosion)  # Add explosion to the explosion group

                # Check if the player is within the blast radius (2 tile size)
                if abs(self.rect.centerx - screen.get_player().rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - screen.get_player().rect.centery) < TILE_SIZE * 2:
                    screen.get_player().health -= 25  # Deal 25 damage to the player

                # Check for enemies within the blast radius and apply damage
                for enemy in screen.get_enemy_group():
                    if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                        enemy.health -= 75  # Deal 75 damage to enemies in the blast radius
