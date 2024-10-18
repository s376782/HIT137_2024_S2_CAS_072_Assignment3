import pygame
from widgets.itembox_tile import ItemBoxTile
from widgets.decoration_tile import DecorationTile
from widgets.exit_tile import ExitTile
from widgets.water_tile import WaterTile
from widgets.character import Boss, Enemy, Player
from widgets.tile import Tile

class TileManager:
    """
    TileManager is responsible for creating and managing different types of tiles and game objects.
    It organizes tiles into groups for easier management, such as walls, water, decorations, enemies, etc.
    """

    def __init__(self):
        """
        Initialize the TileManager with various sprite groups to organize different tile types.
        """
        self.tile_group = pygame.sprite.Group()  # Group for all tiles
        self.wall_group = pygame.sprite.Group()  # Group for wall tiles
        self.water_group = pygame.sprite.Group()  # Group for water tiles
        self.decoration_group = pygame.sprite.Group()  # Group for decoration tiles
        self.enemy_group = pygame.sprite.Group()  # Group for enemy characters
        self.item_box_group = pygame.sprite.Group()  # Group for item boxes (health, arrows, bombs)
        self.exit_group = pygame.sprite.Group()  # Group for exit tiles
        self.player = None  # Player instance will be stored here

    def create_tile(self, tileId, x, y) -> (Tile | None):
        """
        Create a tile or game object based on its tileId and add it to the appropriate group.
        :param tileId: An integer ID representing the type of tile to create.
        :param x: The x-coordinate where the tile will be placed.
        :param y: The y-coordinate where the tile will be placed.
        :return: The created tile object, or None if no tile was created.
        """
        tile = None  # Initialize the tile object as None

        # Check tileId and create corresponding tile
        if tileId < 0:
            pass  # Do nothing for invalid tileId
        elif tileId >= 0 and tileId < 9: # Wall tiles (tileId from 0 to 8)
            tile = Tile(tileId, x, y)
            self.wall_group.add(tile)
        elif tileId >= 9 and tileId < 11: # Water tiles (tileId 9 and 10)
            tile = WaterTile(tileId, x, y)
            self.water_group.add(tile)
        elif tileId >= 11 and tileId < 15: # Decoration tiles (tileId from 11 to 14)
            tile = DecorationTile(tileId, x, y)
            self.decoration_group.add(tile)
        elif tileId == 15: # Player tile (tileId 15)
            self.player = tile = Player(tileId, x, y)
        elif tileId == 16: # Enemy tile (tileId 16)
            tile = Enemy(tileId, x, y)
            self.enemy_group.add(tile)
        elif tileId == 17: # Arrow item box (tileId 17)
            tile = ItemBoxTile.create_arrow_box(tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 18: # Bomb item box (tileId 18)
            tile = ItemBoxTile.create_bomb_box(tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 19: # Health item box (tileId 19)
            tile = ItemBoxTile.create_health_box(tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 20: # Exit tile (tileId 20)
            tile = ExitTile(tileId, x, y)
            self.exit_group.add(tile)
        elif tileId == 21: # Boss enemy tile (tileId 21)
            tile = Boss(tileId, x, y)
            self.enemy_group.add(tile)

        # If a tile was created, add it to the general tile group
        if tile is not None:
            self.tile_group.add(tile)

        return tile  # Return the created tile, or None if no tile was created
