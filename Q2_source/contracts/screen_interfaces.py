import pygame

class IPlayer:
    pass

class IScrollScreen:
    def get_screen_scroll(self) -> int:
        raise NotImplementedError

    def get_bg_scroll(self) -> int:
        raise NotImplementedError

class IPlayScreen(IScrollScreen):
    def get_level_length(self) -> int:
        raise NotImplementedError

    def get_player(self) -> IPlayer:
        raise NotImplementedError

    def get_obstacle_group(self) -> pygame.sprite.Group:
        raise NotImplementedError

    def get_enemy_group(self) -> pygame.sprite.Group:
        raise NotImplementedError
    
    def get_water_group(self) -> pygame.sprite.Group:
        raise NotImplementedError

    def get_exit_group(self) -> pygame.sprite.Group:
        raise NotImplementedError
    
    def get_bullet_group(self) -> pygame.sprite.Group:
        raise NotImplementedError