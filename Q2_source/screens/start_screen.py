#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
from screens.base_screen import BaseScreen
from widgets.button import ExitButton, StartButton
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class StartScreen(BaseScreen):
    """
    StartScreen is the main screen presented to the player when they start the game.
    It contains a Start button to begin the game and an Exit button to close the game.
    """

    def __init__(self, onStart, onExit):
        """
        Initialize the StartScreen object.
        :param onStart: A callback function that will be executed when the Start button is clicked.
        :param onExit: A callback function that will be executed when the Exit button is clicked.
        """
        super().__init__()

        # Add the Start and Exit buttons to the screen's sprite group
        self.sprites.add(
            StartButton(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, onStart),
            ExitButton(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, onExit)
        )
