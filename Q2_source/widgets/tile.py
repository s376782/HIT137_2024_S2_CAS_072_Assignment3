#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
import pygame
from typing import override
from contracts.screen_interfaces import IScrollScreen
from settings import TILE_SIZE, TILE_TYPES

# Load all tile images and resize them to the TILE_SIZE
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile/{x}.png')  # Load each tile image based on its index
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))  # Resize the image to fit the tile size
    img_list.append(img)  # Append the processed image to the list

# Tile class inherits from pygame's Sprite class
class Tile(pygame.sprite.Sprite):
    """
    The Tile class represents a single tile in the game.
    It uses the Pygame Sprite class to handle tile behavior and interactions with the screen.
    """

    def __init__(self, tile, x, y):
        """
        Initialize the Tile object.
        :param tile: Index of the tile type (used to select the appropriate image from img_list).
        :param x: The x-coordinate where the tile should be placed.
        :param y: The y-coordinate where the tile should be placed.
        """
        super().__init__()
        self.image = img_list[tile]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    @override
    def update(self, *args, **kwargs):
        """
        Update method called every frame to update the tile's position or behavior.
        In this case, it adjusts the tile's position based on screen scroll.
        """
        super().update(*args, **kwargs)

        # Ensure we get the screen object from the arguments and check if it supports scrolling
        screen = args[0]
        if screen and isinstance(screen, IScrollScreen):
            # Adjust the tile's position by the amount of screen scroll
            self.rect.x += screen.get_screen_scroll()