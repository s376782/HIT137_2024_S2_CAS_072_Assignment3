import pygame
from widgets.itembox_tile import ItemBoxTile
from widgets.decoration_tile import DecorationTile
from widgets.exit_tile import ExitTile
from widgets.water_tile import WaterTile
from widgets.character import Enemy, Character
from widgets.tile import Tile

class TileManager:
    def __init__(self):
        self.tile_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()

    def create_tile(self, tileId, x, y) -> (Tile | None):
        tile = None

        if tileId < 0:
            pass
        elif tileId >= 0 and tileId < 9:
            tile = Tile(tileId, x, y)
            self.wall_group.add(tile)
        elif tileId >= 9 and tileId < 11:
            tile = WaterTile(tileId, x, y)
            self.water_group.add(tile)
        elif tileId >= 11 and tileId < 15:
            tile = DecorationTile(tileId, x, y)
            self.decoration_group.add(tile)
        elif tileId == 15: # create player
            self.player = tile = Character(tileId, x, y)
        elif tileId == 16: # create enemy
            tile = Enemy(tileId, x, y)
            self.enemy_group.add(tile)
        elif tileId == 17: # create arrow box
            tile = ItemBoxTile.create_arrow_box(tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 18: # create bomb box
            tile = ItemBoxTile.create_bomb_box(tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 19: # create health box
            tile = ItemBoxTile.create_health_box(tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 20: #create exit
            tile = ExitTile(tileId, x, y)
            self.exit_group.add(tile)

        if tile is not None:
            self.tile_group.add(tile)

        return tile