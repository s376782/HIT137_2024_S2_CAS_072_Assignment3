import pygame
from typing import override
from contracts.screen_interfaces import IPlayerScreen
from widgets.tile import Tile

ItemType_Health = 'Health'
ItemType_Ammo = 'Ammo'
ItemType_Grenade = 'Grenade'

class ItemBoxTile(Tile):
    def __init__(self, item_type, tile, x, y):
        super().__init__(tile, x, y)
        self.item_type = item_type

    @override
    def update(self, *args, **kwargs):
        super().update(args, kwargs)
        screen = args[0]
        if screen and isinstance(screen, IPlayerScreen):
            #check if the player has picked up the box
            player = screen.get_player()
            if pygame.sprite.collide_rect(self, player):
                # check what kind of box it was
                if self.item_type == ItemType_Health:
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                elif self.item_type == ItemType_Ammo:
                    player.ammo += 15
                elif self.item_type == ItemType_Grenade:
                    player.grenades += 3

                #delete the item box
                self.kill()