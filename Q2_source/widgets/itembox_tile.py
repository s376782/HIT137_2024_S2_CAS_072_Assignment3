import pygame
from typing import override
from widgets.tile import Tile
from contracts.screen_interfaces import IPlayScreen

class ItemBoxTile(Tile):
    ItemType_Health = 'Health'
    ItemType_Ammo = 'Ammo'
    ItemType_Grenade = 'Grenade'

    @staticmethod
    def create_health_box(tile, x, y):
        return ItemBoxTile(ItemBoxTile.ItemType_Health, tile, x, y)

    @staticmethod
    def create_ammo_box(tile, x, y):
        return ItemBoxTile(ItemBoxTile.ItemType_Ammo, tile, x, y)

    @staticmethod
    def create_grenade_box(tile, x, y):
        return ItemBoxTile(ItemBoxTile.ItemType_Grenade, tile, x, y)

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
                elif self.item_type == ItemBoxTile.ItemType_Ammo:
                    player.ammo += 15
                elif self.item_type == ItemBoxTile.ItemType_Grenade:
                    player.grenades += 3

                #delete the item box
                self.kill()