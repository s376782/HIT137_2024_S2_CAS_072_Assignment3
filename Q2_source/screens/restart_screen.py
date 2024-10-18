#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
from typing import override
from screens.base_screen import BaseScreen
from widgets.button import RestartButton, ExitButton
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class RestartScreen(BaseScreen):
    """
    The RestartScreen class is shown when the game ends, either due to a game over or game completion.
    It contains buttons to restart the game or exit, and displays a message depending on the game's outcome.
    """

    def __init__(self, onRestart, onExit, game_completed=False):
        """
        Initialize the RestartScreen object.
        :param onRestart: A callback function that will be executed when the Restart button is clicked.
        :param onExit: A callback function that will be executed when the Exit button is clicked.
        :param game_completed: Boolean flag indicating if the game was completed (True) or lost (False).
        """
        super().__init__()

        # Add Restart and Exit buttons to the sprite group
        self.sprites.add(
            RestartButton(SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 50, onRestart, 3),
            ExitButton(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 100, onExit)
        )

        # Initialize font and game over message
        self.font = pygame.font.SysFont('Futura', 50)
        self.game_over_text = "Game Completed! You saved the princess" if game_completed else "Game Over!"

    @override
    def draw_background(self, screen: pygame.Surface):
        """
        Draw the background of the restart screen, including the game over/completion message.
        :param screen: The Pygame surface where the elements will be drawn.
        """
        # Draw the background using the parent class method
        super().draw_background(screen)
        
        # Render the game over/completion message in red color
        text_surface = self.font.render(self.game_over_text, True, (255, 0, 0))  # Red text

        # Position the text at the center of the screen, one third down the height
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        # Draw the game over/completion message on the screen
        screen.blit(text_surface, text_rect)
