#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
import pygame
from typing import List
from settings import BG

class BaseScreen:
    """
    The BaseScreen class serves as a base class for all game screens.
    It manages common functionality like handling events, updating, and drawing sprites and backgrounds.
    """

    def __init__(self):
        """
        Initialize the BaseScreen object.
        Sets up a default sprite group to manage all game objects (sprites) that will be updated and drawn.
        """
        # Create a default sprite group to hold all sprites that belong to this screen
        self.sprites = pygame.sprite.Group()

    def handle_events(self, events: List[pygame.event.Event]):
        """
        Handle user input events such as keyboard presses, mouse clicks, etc.
        :param events: List of Pygame events.
        """
        # This method can be overridden by subclasses to handle specific events
        pass

    def update(self):
        """
        Update the state of all sprites in the screen.
        Calls the update method for all sprites within the sprite group.
        """
        # Update all sprites in the group
        self.sprites.update(self)

    def draw_background(self, screen: pygame.Surface):
        """
        Draw the background of the screen.
        By default, it fills the screen with a background color (BG).
        :param screen: The surface on which the background will be drawn.
        """
        screen.fill(BG)  # Fill the screen with the background color

    def draw_sprites(self, screen: pygame.Surface):
        """
        Draw all sprites in the sprite group on the screen.
        :param screen: The surface on which the sprites will be drawn.
        """
        # Draw all sprites from the sprite group onto the screen surface
        self.sprites.draw(screen)

    def draw(self, screen: pygame.Surface):
        """
        Draw both the background and the sprites on the screen.
        This method combines drawing the background and sprites.
        :param screen: The surface on which the background and sprites will be drawn.
        """
        # Draw the background first, then draw all sprites
        self.draw_background(screen)
        self.draw_sprites(screen)
        


