import pygame

from screens.game_play_screen import GamePlayScreen
from screens.restart_screen import RestartScreen
from screens.start_screen import StartScreen

class Game:
    def __init__(self):
        self.running = True
        self.current_screen = StartScreen(self.onStart, self.onExit)

    def onStart(self):
        self.current_screen = GamePlayScreen(self.onPlayerDie)
        self.current_screen.load_level(1)

    def onExit(self):
        self.running = False

    def onPlayerDie(self):
        self.current_screen = RestartScreen(self.onStart)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            # keyboard presses
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        self.current_screen.handle_events(events)

    def update(self):
        self.current_screen.update()

    def draw(self, screen: pygame.Surface):
        self.current_screen.draw(screen)
