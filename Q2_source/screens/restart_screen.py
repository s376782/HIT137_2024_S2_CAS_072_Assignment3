from screens.base_screen import BaseScreen
from widgets.button import RestartButton
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class RestartScreen(BaseScreen):
	def __init__(self, onRestart):
		BaseScreen.__init__(self)
		self.sprites.add(
			RestartButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, onRestart, 2)
		)