import pygame
from typing import override
from contracts.screen_interfaces import IPlayScreen
from settings import BLACK, GREEN, MAX_HEALTH, RED, SCREEN_HEIGHT, SCREEN_WIDTH

# Create Health bar
class HealthBar(pygame.sprite.Sprite):
    """
    The HealthBar class represents a visual health bar displayed on the screen.
    It updates in real-time based on the player's current health.
    """

    def __init__(self, x, y):
        """
        Initialize the HealthBar object.
        :param x: The x-coordinate for the health bar's position.
        :param y: The y-coordinate for the health bar's position.
        """
        super().__init__()
        self.x = x  # Horizontal position of the health bar
        self.y = y  # Vertical position of the health bar
        self.update_image(0)  # Initialize the health bar with 0 health

    def update_image(self, health):
        """
        Update the health bar's visual appearance based on the player's current health.
        :param health: The player's current health.
        """
        self.health = health  # Store the current health
        ratio = self.health / MAX_HEALTH  # Calculate the health ratio (0.0 to 1.0)

        # Create a transparent surface for the health bar
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()

        # Draw the health bar's background (black border)
        pygame.draw.rect(self.image, BLACK, (self.x - 2, self.y - 2, 154, 24))

        # Draw the empty portion of the health bar (red background)
        pygame.draw.rect(self.image, RED, (self.x, self.y, 150, 20))

        # Draw the filled portion of the health bar (green foreground based on health ratio)
        pygame.draw.rect(self.image, GREEN, (self.x, self.y, 150 * ratio, 20))        

    @override
    def update(self, *args, **kwargs):
        """
        Update the health bar every frame to reflect the player's current health.
        """
        super().update(*args, **kwargs)

        # Get the screen object (game screen interface)
        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            player = screen.get_player()
            if player and self.health != player.health:
                # If the player's health has changed, update the health bar
                self.update_image(player.health)