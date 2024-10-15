import pygame
from typing import List
from settings import BG

class BaseScreen:
	def __init__(self):
        # Default sprite group
		self.sprites = pygame.sprite.Group()

	def handle_events(self, events: List[pygame.event.Event]):
		pass

	def update(self):
		self.sprites.update(self)

	def draw_background(self, screen: pygame.Surface):
		screen.fill(BG)

	def draw_sprites(self, screen: pygame.Surface):
		self.sprites.draw(screen)

	def draw(self, screen: pygame.Surface):
		self.draw_background(screen)
		self.draw_sprites(screen)
		


