import pygame
from typing import override
from widgets.tile import Tile
from contracts.screen_interfaces import IPlayScreen

class ItemBoxTile(Tile):
    ItemType_Health = 'Health'
    ItemType_Arrow = 'Arrow'
    ItemType_Bomb = 'Bomb'

    @staticmethod
    def create_health_box(tile, x, y):
        return ItemBoxTile(ItemBoxTile.ItemType_Health, tile, x, y)

    @staticmethod
    def create_arrow_box(tile, x, y):
        return ItemBoxTile(ItemBoxTile.ItemType_Arrow, tile, x, y)

    @staticmethod
    def create_bomb_box(tile, x, y):
        return ItemBoxTile(ItemBoxTile.ItemType_Bomb, tile, x, y)

    def __init__(self, item_type, tile, x, y):
        super().__init__(tile, x, y)
        self.item_type = item_type

    @override
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            #check if the player has picked up the box
            player = screen.get_player()
            if pygame.sprite.collide_rect(self, player):
                # check what kind of box it was
                if self.item_type == ItemBoxTile.ItemType_Health:
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                elif self.item_type == ItemBoxTile.ItemType_Arrow:
                    player.arrow += 15
                elif self.item_type == ItemBoxTile.ItemType_Bomb:
                    player.bombs += 3

                #delete the item box
                self.kill()