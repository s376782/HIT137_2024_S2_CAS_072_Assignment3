from screens.base_screen import BaseScreen
from widgets.button import RestartButton
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class RestartScreen(BaseScreen):
	def __init__(self, onRestart):
		BaseScreen.__init__(self)
		self.sprites.add(
			RestartButton(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, onRestart, 2)
		)

		# Initialize font and message
		self.font = pygame.font.SysFont('Futura', 60)
		self.game_over_text = "Game Over!"
	
	def draw(self, screen):
        # Call the base screen's draw method to draw background and other elements
		super().draw(screen)
        
        # Render the "Game Over!" text
		text_surface = self.font.render(self.game_over_text, True, (255, 0, 0))  # Red text
		text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        
        # Draw the text to the screen
		screen.blit(text_surface, text_rect)

        # Draw the restart button (or other widgets)
		self.sprites.draw(screen)