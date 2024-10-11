import pygame
from Q2_source.widgets.soldier import Soldier

class IRollScreen:
    def get_screen_scroll(self) -> int:
        pass

class IPlayerScreen:
    def get_player(self) -> Soldier:
        pass

class IPlayScreen(IPlayerScreen):
    def get_obstacle_group(self) -> pygame.sprite.Group:
        pass

    def get_enemy_group(sefl) -> pygame.sprite.Group:
        pass