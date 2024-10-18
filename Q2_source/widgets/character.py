from typing import override
import pygame
import os
import random

from contracts.screen_interfaces import IPlayScreen, IPlayer
from widgets.tile import Tile
from widgets.decoration_tile import DecorationTile
from widgets.arrow import Arrow
from settings import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH, SCROLL_THRESH, TILE_SIZE

jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.05)

# Character class: Base class for Player, Enemy, and Boss
class Character(Tile):
    """
    Character class is a base class for all characters, including players, enemies, and bosses.
    It handles common functionality such as movement, jumping, shooting, animations, and health.
    """

    def __init__(self, tile, char_type, x, y, scale, speed, arrow, bombs):
        """
        Initialize the Character object.
        :param tile: The tile index for the character.
        :param char_type: Type of the character ('player', 'enemy', etc.).
        :param x: Initial x-coordinate of the character.
        :param y: Initial y-coordinate of the character.
        :param scale: Scale factor for the character sprite.
        :param speed: Movement speed of the character.
        :param arrow: Initial amount of arrows the character has.
        :param bombs: Initial amount of bombs the character has.
        """
        super().__init__(tile, x, y)
        self.alive = True
        self.char_type = char_type
        self.speed = speed  # Movement speed of the character
        self.arrow = arrow  # Number of arrows available
        self.start_arrow = arrow
        self.shoot_cooldown = 0  # Cooldown timer for shooting
        self.bombs = bombs
        self.health = 100  # Initial health of the character
        self.max_health = self.health
        self.direction = 1  # 1 for right, -1 for left
        self.vel_y = 0  # Vertical velocity (used for jumping/falling)
        self.jump = False
        self.in_air = True  # Track if the character is in the air
        self.flip = False  # Flip the image when moving left
        self.action = 0  # Current action (animation state)
        self.update_time = pygame.time.get_ticks()

        # Load all animation frames for the character
        self.animation_list = []
        self.frame_index = 0
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    @override
    def update(self, *args, **kwargs):
        """
        Update method called every frame.
        Manages animations, alive status, and cooldowns.
        """
        if self.char_type == 'enemy':
            pass

        if self.char_type != 'player':
            super().update(*args, **kwargs)

        # Update character animations and check if alive
        self.update_animation()
        self.check_alive()

        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def movement(self, screen: IPlayScreen, moving_left: bool, moving_right: bool):
        """
        Handle the character's movement including jumping, falling, and collisions.
        :param screen: The game screen interface.
        :param moving_left: Whether the character is moving left.
        :param moving_right: Whether the character is moving right.
        :return: A tuple with the screen scroll value and whether the level is completed.
        """
        screen_scroll = 0
        dx = 0
        dy = 0

        # Move left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jumping logic
        if self.char_type == 'player' and self.jump == True and self.in_air == False:
            self.vel_y = -11  # Jump strength
            dx += self.direction * 2 * TILE_SIZE
            self.jump = False
            self.in_air = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10  # Limit fall speed
        dy += self.vel_y

        # Collision detection with obstacles
        for tile in screen.get_obstacle_group():
            # Check for collisions in the x-direction (horizontal movement)
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0  # Stop horizontal movement on collision
                # Reverse direction for AI enemies upon hitting a wall
                if self.char_type == 'enemy':
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter = 0

            # Check for collisions in the y-direction (vertical movement)
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:  # Jumping collision
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                elif self.vel_y >= 0:  # Falling collision
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile.rect.top - self.rect.bottom

        # Check for collision with water or exit
        if pygame.sprite.spritecollide(self, screen.get_water_group(), False):
            self.health = 0  # Character dies if falling into water

        # Check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, screen.get_exit_group(), False):
            level_complete = True  # Character reaches the exit

        # Check if character fell off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        # Check for screen scrolling when moving
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'player':
            if (
                self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and screen.get_bg_scroll() <
                (screen.get_level_length() * TILE_SIZE) - SCREEN_WIDTH
               ) or (self.rect.left < SCROLL_THRESH and screen.get_bg_scroll() > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self, screen: IPlayScreen):
        if self.shoot_cooldown == 0 and self.arrow > 0:
            self.shoot_cooldown = 20
            bullet = Arrow(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), 
                           self.rect.centery, self.direction)
            screen.get_arrow_group().add(bullet)
            #reduce arrow
            self.arrow -= 1
            shot_fx.play()

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)   # Death action


class Enemy(Character):
    def __init__(self, tile, x, y, scale=0.5, speed=2, arrow=20, bombs=0):
        super().__init__(tile, 'enemy', x, y, scale, speed, arrow, bombs)
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

    def ai(self, screen: IPlayScreen):
        player = screen.get_player()
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
            #check if the ai in near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0: idle
                #shoot
                self.shoot(screen)
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.movement(screen, ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        #scroll
        self.rect.x += screen.get_screen_scroll()

    @override
    def update(self, *args, **kwargs):
        screen = args[0]
        if screen and isinstance(screen, IPlayScreen):
            self.ai(screen)
        super().update(*args, **kwargs)


class Player(Character, IPlayer):
    def __init__(self, tile, x, y):
        Character.__init__(self, tile, 'player', x, y, 1.5, 7, 20, 5)   # scale: 1.5 Speed: 7, arrow: 20, bombs:5
        self.lives = 3    # The player has 3 lives
    
    def respawn(self):
        self.alive = True
        self.health = self.max_health  # Reset health to max health

# Create boss enemy with health = 300
class Boss(Enemy):
    def __init__(self, tile, x, y, scale=1, speed=1, arrow=30, bombs=0):
        super().__init__(tile, x, y, scale, speed, arrow, bombs)
        self.flip = True
        self.health = 300
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vision = pygame.Rect(0, 0, 150, 20)

    @override
    def ai(self, screen):    
        player = screen.get_player()
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50

            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0: idle
                #shoot
                self.shoot(screen) 
            else: 
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.movement(screen, False, False)
                    self.update_action(1)  #1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    @override
    def movement(self, screen: IPlayScreen, moving_left: bool, moving_right: bool):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            self.flip = True
            self.direction = -1
        if moving_right:
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            dx += self.direction * 2 * TILE_SIZE
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in screen.get_obstacle_group():
            # check if this tile is the current enemy itself and skip collision check
            if tile == self or isinstance(tile, DecorationTile):
                continue
            #check collision in the x direction
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    # only reverse direction after moving a certain distance or time
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter = 0      # reset move counter after reversing
            #check for collision in the y direction
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile.rect.bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile.rect.top - self.rect.bottom

        #check for collision with water
        if pygame.sprite.spritecollide(self, screen.get_water_group(), False):
            self.health = 0

        #check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, screen.get_exit_group(), False):
            level_complete = True

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0


        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'player':
            if (
                self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and screen.get_bg_scroll() <
                (screen.get_level_length() * TILE_SIZE) - SCREEN_WIDTH
               ) or (self.rect.left < SCROLL_THRESH and screen.get_bg_scroll() > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete    
