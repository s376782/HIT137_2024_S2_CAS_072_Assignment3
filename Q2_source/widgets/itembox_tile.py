import pygame
from typing import override
from widgets.tile import Tile
from contracts.screen_interfaces import IPlayScreen


# Collectible items represented as tiles
class ItemBoxTile(Tile):
    """
    ItemBoxTile is a subclass of Tile representing collectible items that the player can interact with.
    Each item box can provide different rewards to the player (e.g., health, arrows, or bombs).
    """

    # Constants representing the types of items that can be found in an item box
    ItemType_Health = 'Health'
    ItemType_Arrow = 'Arrow'
    ItemType_Bomb = 'Bomb'

    # Static methods to create specific item boxes
    @staticmethod
    def create_health_box(tile, x, y):
        """
        Factory method to create a Health item box.
        :param tile: The tile index representing the health box image.
        :param x: The x-coordinate where the health box is placed.
        :param y: The y-coordinate where the health box is placed.
        :return: An instance of ItemBoxTile with the health type.
        """
        return ItemBoxTile(ItemBoxTile.ItemType_Health, tile, x, y)

    @staticmethod
    def create_arrow_box(tile, x, y):
        """
        Factory method to create an Arrow item box.
        :param tile: The tile index representing the arrow box image.
        :param x: The x-coordinate where the arrow box is placed.
        :param y: The y-coordinate where the arrow box is placed.
        :return: An instance of ItemBoxTile with the arrow type.
        """
        return ItemBoxTile(ItemBoxTile.ItemType_Arrow, tile, x, y)

    @staticmethod
    def create_bomb_box(tile, x, y):
        """
        Factory method to create a Bomb item box.
        :param tile: The tile index representing the bomb box image.
        :param x: The x-coordinate where the bomb box is placed.
        :param y: The y-coordinate where the bomb box is placed.
        :return: An instance of ItemBoxTile with the bomb type.
        """
        return ItemBoxTile(ItemBoxTile.ItemType_Bomb, tile, x, y)

    def __init__(self, item_type, tile, x, y):
        """
        Initialize the ItemBoxTile object.
        :param item_type: The type of the item contained in the box (Health, Arrow, or Bomb).
        :param tile: The tile index representing the item's visual appearance.
        :param x: The x-coordinate where the item box is placed.
        :param y: The y-coordinate where the item box is placed.
        """
        super().__init__(tile, x, y)
        self.item_type = item_type

    @override
    def update(self, *args, **kwargs):
        """
        Update the ItemBoxTile. In this case, it checks for collisions with the player and
        provides the appropriate item to the player upon collision.
        """
        super().update(*args, **kwargs)

        # Check if the player has collided with the item box
        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            #check if the player has picked up the box
            player = screen.get_player()
            if pygame.sprite.collide_rect(self, player): # Check if the player has collided with this item box
                # Depending on the item type, modify the player's attributes
                if self.item_type == ItemBoxTile.ItemType_Health:
                    player.health += 25 # Add 25 health
                    if player.health > player.max_health: # Ensure the player's health does not exceed the maximum
                        player.health = player.max_health
                elif self.item_type == ItemBoxTile.ItemType_Arrow:
                    player.arrow += 15 # Add 15 arrows
                elif self.item_type == ItemBoxTile.ItemType_Bomb:
                    player.bombs += 3 # Add 3 bombs

                # Remove the item box from the game after it has been collected
                self.kill()