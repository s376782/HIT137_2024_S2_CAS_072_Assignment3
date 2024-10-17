import pygame

from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

class Game:
    def onStart(self):
        from screens.game_play_screen import GamePlayScreen
        self.current_screen = GamePlayScreen(self.onPlayerDie, self.onGameCompleted)
        self.current_screen.load_level(1)

    def onExit(self):
        self.__running = False

    def onPlayerDie(self):
        from screens.restart_screen import RestartScreen
        self.current_screen = RestartScreen(self.onStart, self.onExit)

    def onGameCompleted(self):
        from screens.restart_screen import RestartScreen
        self.current_screen = RestartScreen(self.onStart, self.onExit, True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.__running = False

            # keyboard presses
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__running = False

        self.current_screen.handle_events(events)

    def update(self):
        self.current_screen.update()

    def draw(self, screen: pygame.Surface):
        self.current_screen.draw(screen)

    def run(self):
        pygame.init()
        pygame.mixer.init()

        # Window name (title)
        pygame.display.set_caption("Save the Princess")

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        from screens.start_screen import StartScreen
        self.current_screen = StartScreen(self.onStart, self.onExit)

        self.__running = True
        while self.__running:
            clock.tick(FPS)

            self.handle_events(pygame.event.get())
            self.update()
            self.draw(screen)

            pygame.display.update()

        pygame.quit()