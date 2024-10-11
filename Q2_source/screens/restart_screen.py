from screens.base_screen import BaseScreen
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from widgets.button import RestartButton

class RestartScreen(BaseScreen):
	def __init__(self, onRestart):
		BaseScreen.__init__(self)
		self.sprites.add(
			RestartButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, onRestart)
		)