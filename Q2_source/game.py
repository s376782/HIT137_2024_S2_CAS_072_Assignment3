#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
import pygame

from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

class Game:
    """
    The Game class is the main engine for managing the game's flow. It handles starting the game,
    player death, game completion, updating the game state, and switching between screens.
    """

    def onStart(self):
        """
        Initialize and load the GamePlayScreen when the player starts the game.
        """
        from screens.game_play_screen import GamePlayScreen
        self.current_screen = GamePlayScreen(self.onPlayerDie, self.onGameCompleted)
        self.current_screen.load_level(1)

    def onExit(self):
        """
        Exit the game when the exit button is pressed or when the game is closed.
        """
        self.__running = False

    def onPlayerDie(self):
        """
        Handle the player's death by switching to the RestartScreen.
        """
        from screens.restart_screen import RestartScreen
        self.current_screen = RestartScreen(self.onStart, self.onExit)

    def onGameCompleted(self):
        """
        Handle the game completion event by switching to the RestartScreen with a game-completed message.
        """
        from screens.restart_screen import RestartScreen
        self.current_screen = RestartScreen(self.onStart, self.onExit, True)

    def handle_events(self, events):
        """
        Handle global events like quitting the game or pressing escape. Pass other events to the current screen.
        :param events: List of Pygame events.
        """
        for event in events:
            if event.type == pygame.QUIT: # Quit event
                self.__running = False

            # Quit the game if the escape key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.__running = False

        # Pass the events to the current screen's event handler
        self.current_screen.handle_events(events)

    def update(self):
        """
        Update the current screen, handling all updates (gameplay, animations, etc.).
        """
        self.current_screen.update()

    def draw(self, screen: pygame.Surface):
        """
        Draw the current screen, rendering all visuals.
        :param screen: The Pygame surface to draw on.
        """
        self.current_screen.draw(screen)

    def run(self):
        """
        Main game loop that handles initializing, updating, drawing, and quitting the game.
        """
        pygame.init()  # Initialize Pygame
        pygame.mixer.init()  # Initialize sound mixer

        # Set the window title
        pygame.display.set_caption("Save the Princess")

        # Create the game window with the specified width and height
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        # Load the StartScreen at the beginning of the game
        from screens.start_screen import StartScreen
        self.current_screen = StartScreen(self.onStart, self.onExit)

        self.__running = True  # Game loop control flag
        while self.__running:
            clock.tick(FPS)  # Limit the frame rate to the specified FPS

            # Handle all events (input, window events, etc.)
            self.handle_events(pygame.event.get())
            self.update()  # Update the game state
            self.draw(screen)  # Render the game screen

            pygame.display.update()  # Update the display with new drawings

        pygame.quit()  # Quit Pygame after the game loop ends
