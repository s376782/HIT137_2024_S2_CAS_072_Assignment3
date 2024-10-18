from screens.base_screen import BaseScreen
from widgets.button import RestartButton, ExitButton
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame

class RestartScreen(BaseScreen):
	def __init__(self, onRestart, onExit, game_completed=False):
		BaseScreen.__init__(self)
		self.sprites.add(
			RestartButton(SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 50, onRestart, 3),
			ExitButton(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 100, onExit)
		)

		# Initialize font and message
		self.font = pygame.font.SysFont('Futura', 50)
		self.game_over_text = "Game Completed! You saved the princess" if game_completed else "Game Over!"
		
			
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