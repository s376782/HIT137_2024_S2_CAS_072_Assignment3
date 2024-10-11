from widgets.itembox_tile import ItemBoxTile, ItemType_Health, ItemType_Grenade, ItemType_Ammo
from widgets.decoration_tile import DecorationTile
from widgets.exit_tile import ExitTile
from widgets.water_tile import WaterTile
from widgets.soldier import Enemy, Player, Soldier
from widgets.tile import Tile

import pygame

class TileManager:
    def __init__(self):
        self.tile_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.decoration_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.item_box_group = pygame.sprite.Group()
        self.exit_group = pygame.sprite.Group()

    def create_tile(self, tileId, x, y) -> Tile:
        if tileId < 0:
            return

        if tileId < 9:
            tile = Tile(tileId, x, y)
            self.wall_group.add(tile)
        elif tileId < 11:
            tile = WaterTile(tileId, x, y)
            self.water_group.add(tile)
        elif tileId < 15:
            tile = DecorationTile(tileId, x, y)
            self.decoration_group.add(tile)
        elif tileId == 15: # create player
            self.player = tile = Player(x, y)
            #self.health_bar = HealthBar(10, 10, self.player.health, self.player.health)
        elif tileId == 16: # create enemy
            tile = Enemy(x, y)
            self.enemy_group.add(tile)
        elif tileId == 17: # create ammo box
            tile = ItemBoxTile(ItemType_Ammo, tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 18: # create grenade box
            tile = ItemBoxTile(ItemType_Grenade, tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 19: # create health box
            tile = ItemBoxTile(ItemType_Health, tileId, x, y)
            self.item_box_group.add(tile)
        elif tileId == 20: #create exit
            tile = ExitTile(tileId, x, y)
            self.exit_group.add(tile)
        if tile:
            self.tile_group.add(tile)
            return tile
        raise ValueError()