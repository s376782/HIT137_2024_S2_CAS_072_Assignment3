import pygame

# Interface for defining player-related behaviors
class IPlayer:
    """
    IPlayer interface defines the required behaviors and properties for a Player.
    Classes implementing this interface should define methods and attributes related 
    to the player character in the game, such as movement, health, and interaction.
    """
    pass

# Interface for screens that support scrolling functionality
class IScrollScreen:
    """
    IScrollScreen interface defines the required methods for handling scrolling behavior on a screen.
    Any class implementing this interface must handle screen scroll and background scroll.
    """
    def get_screen_scroll(self) -> int:
        """
        Returns the current scroll position of the screen (how much the screen has moved).
        This is important for adjusting the view based on the player's movement.
        """
        raise NotImplementedError

    def get_bg_scroll(self) -> int:
        """
        Returns the current background scroll position.
        This is used for parallax effects, where the background moves slower than the foreground.
        """
        raise NotImplementedError

# Interface for a specific type of screen, like a playable game level
class IPlayScreen(IScrollScreen):
    """
    IPlayScreen interface extends IScrollScreen to add specific functionality for a game screen.
    This includes managing level elements, the player, and various groups of obstacles, enemies, etc.
    """

    def get_level_length(self) -> int:
        """
        Returns the total length of the level in pixels. 
        This is useful for determining when the player has reached the end of the level.
        """
        raise NotImplementedError

    def get_player(self) -> IPlayer:
        """
        Returns the player object.
        This allows access to the player instance to check status, position, and interactions.
        """
        raise NotImplementedError

    def get_obstacle_group(self) -> pygame.sprite.Group:
        """
        Returns a group of all obstacles in the level.
        Obstacles could be anything that impedes the player's progress, such as walls or traps.
        """
        raise NotImplementedError

    def get_enemy_group(self) -> pygame.sprite.Group:
        """
        Returns a group of all enemy sprites in the level.
        This group will be used for handling interactions between the player and enemies (e.g., collisions).
        """
        raise NotImplementedError
    
    def get_water_group(self) -> pygame.sprite.Group:
        """
        Returns a group of water-related sprites in the level.
        Water might behave differently, such as slowing down the player or causing damage.
        """
        raise NotImplementedError

    def get_exit_group(self) -> pygame.sprite.Group:
        """
        Returns a group of exit points in the level.
        These could represent the goal or checkpoint the player needs to reach to complete the level.
        """
        raise NotImplementedError
    
    def get_arrow_group(self) -> pygame.sprite.Group:
        """
        Returns a group of arrow sprites in the level.
        Arrows could be projectiles or indicators guiding the player through the level.
        """
        raise NotImplementedError