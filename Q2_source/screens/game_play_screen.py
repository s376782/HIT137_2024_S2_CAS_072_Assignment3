import csv
import pygame

from typing import List, override
from pygame.event import Event
from pygame.sprite import Group

from screens.base_screen import BaseScreen
from screens.tile_manager import TileManager
from contracts.screen_interfaces import IPlayScreen
from widgets.bomb import Bomb
from widgets.health_bar import HealthBar
from settings import SCREEN_HEIGHT, TILE_SIZE

pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

class GamePlayScreen(BaseScreen, IPlayScreen):
    def __init__(self, onPlayerDie):
        super().__init__()
        self.sprites.add(
            HealthBar(10, 10)
        )

        self.bomb_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.arrow_group = pygame.sprite.Group()
        self.bg_scroll = 0
        self.screen_scroll = 0

        self.shoot = False
        self.bomb = False 
        self.bomb_thrown = False
        self.moving_left = self.moving_right = False

    @override
    def get_screen_scroll(self) -> int:
        return self.screen_scroll

    @override
    def get_bg_scroll(self) -> int:
        return self.bg_scroll

    @override
    def get_level_length(self) -> int:
        return self.level_length

    @override
    def get_player(self):
        return self.player

    @override
    def get_obstacle_group(self) -> Group:
        return self.tile_manager.wall_group

    @override
    def get_enemy_group(self) -> Group:
        return self.tile_manager.enemy_group

    @override
    def get_water_group(self) -> Group:
        return self.tile_manager.water_group

    @override
    def get_exit_group(self) -> Group:
        return self.tile_manager.exit_group
    
    @override
    def get_arrow_group(self) -> Group:
        return self.arrow_group

    def load_level(self, level: int):
        world_data = []
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for x, row in enumerate(reader):
                rowData = []
                for y, tile in enumerate(row):
                    rowData.append(int(tile))
                world_data.append(rowData)
        self.process_data(world_data)
        self.current_level = level

    def process_data(self, data: List[List[int]]):
        self.level_length = len(data[0])
        self.tile_manager = TileManager()
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                self.tile_manager.create_tile(tile, x*TILE_SIZE, y*TILE_SIZE)

        self.player = self.tile_manager.player        
        self.health_bar = HealthBar(10, 10)

    @override
    def update(self):
        super().update()

        self.tile_manager.tile_group.update(self)
        self.bomb_group.update(self)
        self.explosion_group.update(self)
        self.arrow_group.update(self)

        if self.player.alive:
            #shoot bullets
            if self.shoot:
                self.player.shoot(self)
            #throw grenades
            elif self.bomb and self.bomb_thrown == False and self.player.bombs > 0:
                bomb = Bomb(self.player.rect.centerx + (0.5 * self.player.rect.size[0] * self.player.direction),
                                  self.player.rect.top,
                                  self.player.direction)
                self.bomb_group.add(bomb)
                #reduce grenades
                self.player.bombs -= 1
                self.bomb_thrown = True
            if self.player.in_air:
                self.player.update_action(2)#2: jump
            elif self.moving_left or self.moving_right:
                self.player.update_action(1) #1: run
            else:
                self.player.update_action(0) #0: idle
            self.screen_scroll, self.level_complete = self.player.movement(self, self.moving_left, self.moving_right)
            self.bg_scroll -= self.screen_scroll
            #check if player has completed the level
            if self.level_complete:
                self.load_level(self.current_level+1)
        else:
            self.screen_scroll = 0

        # check for uplevel
        level_complete = False
        if pygame.sprite.spritecollide(self.player, self.tile_manager.exit_group, False):
            level_complete = True

    @override
    def draw_background(self, screen: pygame.Surface):
        super().draw_background(screen)
        width = sky_img.get_width()
        for x in range(5):
            screen.blit(sky_img, ((x * width) - self.bg_scroll * 0.5, 0))
            screen.blit(mountain_img, ((x * width) - self.bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
            screen.blit(pine1_img, ((x * width) - self.bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
            screen.blit(pine2_img, ((x * width) - self.bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

    @override
    def draw_sprites(self, screen: pygame.Surface):
        super().draw_sprites(screen)
        self.arrow_group.draw(screen)
        self.bomb_group.draw(screen)
        self.explosion_group.draw(screen)
        self.tile_manager.tile_group.draw(screen)

    @override
    def draw(self, screen: pygame.Surface):
        super().draw(screen)

        # #show arrow
        # draw_text('ARROW: ', font, WHITE, 10, 35)
        # for x in range(player.arrow):
        #     screen.blit(arrow_img, (90 + (x * 10), 40))
        # #show bombs
        # draw_text('BOMBS: ', font, WHITE, 10, 60)
        # for x in range(player.bombs):
        #     screen.blit(bomb_img, (135 + (x * 15), 60))

    @override
    def handle_events(self, events: List[Event]):
        for event in events:
            # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moving_left = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moving_right = True
                if event.key == pygame.K_SPACE:
                    self.shoot = True
                if event.key == pygame.K_q:
                    self.bomb = True
                if event.key == pygame.K_w and self.player.alive:
                    self.player.jump = True
                    #jump_fx.play()

            # keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.moving_left = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.moving_right = False
                if event.key == pygame.K_SPACE:
                    self.shoot = False
                if event.key == pygame.K_q:
                    self.bomb = False
                    self.bomb_thrown = False
