#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
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
from settings import MAX_LEVELS, SCREEN_HEIGHT, TILE_SIZE, WHITE
from widgets.character import Player

# Load background layers for parallax scrolling
Layer_0000_9_img = pygame.image.load('img/Background/Layer_0000_9.png').convert_alpha()
Layer_0001_8_img = pygame.image.load('img/Background/Layer_0001_8.png').convert_alpha()
Layer_0002_7_img = pygame.image.load('img/Background/Layer_0002_7.png').convert_alpha()
Layer_0003_6_img = pygame.image.load('img/Background/Layer_0003_6.png').convert_alpha()
Layer_0004_Lights_img = pygame.image.load('img/Background/Layer_0004_Lights.png').convert_alpha()
Layer_0005_5_img = pygame.image.load('img/Background/Layer_0005_5.png').convert_alpha()
Layer_0006_4_img = pygame.image.load('img/Background/Layer_0006_4.png').convert_alpha()
Layer_0007_Lights_img = pygame.image.load('img/Background/Layer_0007_Lights.png').convert_alpha()
Layer_0008_3_img = pygame.image.load('img/Background/Layer_0008_3.png').convert_alpha()
Layer_0009_2_img = pygame.image.load('img/Background/Layer_0009_2.png').convert_alpha()
Layer_0010_1_img = pygame.image.load('img/Background/Layer_0010_1.png').convert_alpha()
Layer_0011_0_img = pygame.image.load('img/Background/Layer_0011_0.png').convert_alpha()

class GamePlayScreen(BaseScreen, IPlayScreen):
    """
    GamePlayScreen manages the active game level, player, and interactions
    """

    def __init__(self, onPlayerDie, onGameCompleted):
        """
        Initialize the GamePlayScreen.
        :param onPlayerDie: Callback function to be called when the player dies.
        :param onGameCompleted: Callback function to be called when the game is completed.
        """
        super().__init__()

        # Add a health bar for the player
        self.sprites.add(
            HealthBar(10, 10)
        )

        # Initialize callbacks
        self.onPlayerDie = onPlayerDie
        self.onGameCompleted = onGameCompleted

        # Initialize sprite groups for bombs, explosions, and arrows
        self.bomb_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.arrow_group = pygame.sprite.Group()

        # Initialize background and screen scroll variables
        self.bg_scroll = 0
        self.screen_scroll = 0

        # Player controls
        self.shoot = False
        self.bomb = False 
        self.bomb_thrown = False
        self.moving_left = self.moving_right = False

    # Overridden methods from IPlayScreen interface
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

    # 3 levels
    def load_level(self, level: int):
        """
        Load the level data from a CSV file and initialize the tiles and player.
        :param level: The level number to load.
        """
        # Save the current player's lives (if already exists)
        saved_lives = self.player.lives if hasattr(self, 'player') else 3

        # Load level data from CSV file
        world_data = []
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                world_data.append([int(tile) for tile in row])  # Convert tile values to integers

        # Process the level data and set up tiles and player
        self.process_data(world_data)

        # Restore player's lives and reset scroll values
        self.player.lives = saved_lives
        self.current_level = level
        self.bg_scroll = 0
        self.screen_scroll = 0

    def process_data(self, data: List[List[int]]):
        """
        Process the level data and create tiles and player.
        :param data: A 2D list of tile IDs representing the level layout.
        """
        self.level_length = len(data[0])
        self.tile_manager = TileManager()

        # Iterate through the level data and create tiles
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                self.tile_manager.create_tile(tile, x * TILE_SIZE, y * TILE_SIZE)

        # Set player and health bar
        self.player = self.tile_manager.player        
        self.health_bar = HealthBar(10, 10)

    @override
    def update(self):
        """
        Update the game state and handle player movement, shooting, bombs, and level progression.
        """
        super().update()  # Update sprites and background

        # Update game objects and handle their interactions
        self.tile_manager.tile_group.update(self)
        self.bomb_group.update(self)
        self.explosion_group.update(self)
        self.arrow_group.update(self)

        if self.player.alive:
            # Handle player actions: shooting, throwing bombs, and movement
            if self.shoot:
                self.player.shoot(self)
            elif self.bomb and self.bomb_thrown == False and self.player.bombs > 0:
                bomb = Bomb(self.player.rect.centerx + (0.5 * self.player.rect.size[0] * self.player.direction),
                                  self.player.rect.top,
                                  self.player.direction)
                self.bomb_group.add(bomb)
                self.player.bombs -= 1  # Decrease bomb count
                self.bomb_thrown = True

            # Update player action (idle, run, jump)
            if self.player.in_air:
                self.player.update_action(2)  # Jump action
            elif self.moving_left or self.moving_right:
                self.player.update_action(1)  # Run action
            else:
                self.player.update_action(0)  # Idle action

            # Handle screen scrolling based on player movement
            self.screen_scroll, self.level_complete = self.player.movement(self, self.moving_left, self.moving_right)
            self.bg_scroll -= self.screen_scroll
            #check if player has completed the level
            if self.level_complete:
                if self.current_level < MAX_LEVELS:    
                    self.load_level(self.current_level+1)
                else:
                    self.onGameCompleted()
        else:
            self.screen_scroll = 0
            if self.player.lives > 0:    # Check to reduce player's lives 
                self.player.lives -= 1
                self.player.respawn()     # Restart the current level with full health
                self.load_level(self.current_level)
            if self.player.lives == 0:
                self.onPlayerDie()

        # check for uplevel
        level_complete = False
        if pygame.sprite.spritecollide(self.player, self.tile_manager.exit_group, False):
            level_complete = True

    @override
    def draw_background(self, screen: pygame.Surface):
        super().draw_background(screen)
        width = Layer_0011_0_img.get_width()
        for x in range(5):
            screen.blit(Layer_0011_0_img, ((x * width) - self.bg_scroll * 0.5, 0))
            screen.blit(Layer_0010_1_img, ((x * width) - self.bg_scroll * 0.6, SCREEN_HEIGHT - Layer_0010_1_img.get_height()))
            screen.blit(Layer_0009_2_img, ((x * width) - self.bg_scroll * 0.7, SCREEN_HEIGHT - Layer_0009_2_img.get_height()))
            screen.blit(Layer_0008_3_img, ((x * width) - self.bg_scroll * 0.8, SCREEN_HEIGHT - Layer_0008_3_img.get_height()))
            screen.blit(Layer_0007_Lights_img, ((x * width) - self.bg_scroll * 0.6, SCREEN_HEIGHT - Layer_0007_Lights_img.get_height()))
            screen.blit(Layer_0006_4_img, ((x * width) - self.bg_scroll * 0.7, SCREEN_HEIGHT - Layer_0006_4_img.get_height()))
            screen.blit(Layer_0005_5_img, ((x * width) - self.bg_scroll * 0.8, SCREEN_HEIGHT - Layer_0005_5_img.get_height()))
            screen.blit(Layer_0004_Lights_img, ((x * width) - self.bg_scroll * 0.6, SCREEN_HEIGHT - Layer_0004_Lights_img.get_height()))
            screen.blit(Layer_0003_6_img, ((x * width) - self.bg_scroll * 0.7, SCREEN_HEIGHT - Layer_0003_6_img.get_height()))
            screen.blit(Layer_0002_7_img, ((x * width) - self.bg_scroll * 0.7, SCREEN_HEIGHT - Layer_0002_7_img.get_height()))
            screen.blit(Layer_0001_8_img, ((x * width) - self.bg_scroll * 0.7, SCREEN_HEIGHT - Layer_0001_8_img.get_height()))
            screen.blit(Layer_0000_9_img, ((x * width) - self.bg_scroll * 0.8, SCREEN_HEIGHT - Layer_0000_9_img.get_height()))
        
        #define font
        font = pygame.font.SysFont('Futura', 30)

        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            screen.blit(img, (x, y))

        #show arrow
        draw_text(f'Arrows: {self.player.arrow}', font, WHITE, 10, 35)
        #show bombs
        draw_text(f'Bombs: {self.player.bombs}', font, WHITE, 10, 55)
        #show lives
        draw_text(f'Lives: {self.player.lives}', font, WHITE, 10, 75)


    @override
    def draw_sprites(self, screen: pygame.Surface):
        super().draw_sprites(screen)
        self.arrow_group.draw(screen)
        self.bomb_group.draw(screen)
        self.explosion_group.draw(screen)
        self.tile_manager.tile_group.draw(screen)

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
