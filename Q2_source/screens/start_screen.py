from screens.base_screen import BaseScreen
from widgets.button import ExitButton, StartButton
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class StartScreen(BaseScreen):
    def __init__(self, onStart, onExit):
        super().__init__()
        self.sprites.add(
            StartButton(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, onStart),
            ExitButton(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, onExit)
        )
