#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
import pygame 
from typing import override

# Generic Button class that handles button creation and interaction
class Button(pygame.sprite.Sprite):
    """
    The Button class represents a clickable button in the game.
    It can scale the provided image and triggers a callback function when clicked.
    """

    def __init__(self, x, y, image, callback, scale):
        """
        Initialize the Button object.
        :param x: The x-coordinate for the button's top-left corner.
        :param y: The y-coordinate for the button's top-left corner.
        :param image: The image to be used for the button's appearance.
        :param callback: The function to call when the button is clicked.
        :param scale: The scale factor to apply to the button's image.
        """
        super().__init__()

        # Scale the button image according to the provided scale factor
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        # Get the rectangle area for the button and set its position
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Track whether the button has been clicked to prevent multiple triggers
        self.clicked = False

        # Store the callback function that will be executed when the button is clicked
        self.callback = callback

    @override
    def update(self, *args, **kwargs):
        """
        Update method called every frame to check for button interaction.
        Detects if the button is clicked and triggers the callback function.
        """
        super().update(*args, **kwargs)

        # Get the current mouse position
        pos = pygame.mouse.get_pos()

        # Check if the mouse is hovering over the button and if the left mouse button is clicked
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True  # Mark the button as clicked
            self.callback()  # Call the callback function (button action)

        # Reset the clicked state when the mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

# StartButton is a specialized Button with a predefined start button image
class StartButton(Button):
    """
    A specialized Button class for the start button, using a predefined image.
    """

    def __init__(self, x, y, callback, scale=1):
        """
        Initialize the StartButton with its own image and callback.
        :param x: The x-coordinate for the button's top-left corner.
        :param y: The y-coordinate for the button's top-left corner.
        :param callback: The function to call when the button is clicked.
        :param scale: The scale factor to apply to the button's image (default is 1).
        """
        img = pygame.image.load('img/start_btn.png').convert_alpha()
        super().__init__(x, y, img, callback, scale)

# ExitButton is a specialized Button with a predefined exit button image
class ExitButton(Button):
    """
    A specialized Button class for the exit button, using a predefined image.
    """

    def __init__(self, x, y, callback, scale = 1):
        """
        Initialize the ExitButton with its own image and callback.
        :param x: The x-coordinate for the button's top-left corner.
        :param y: The y-coordinate for the button's top-left corner.
        :param callback: The function to call when the button is clicked.
        :param scale: The scale factor to apply to the button's image (default is 1).
        """
        img = pygame.image.load('img/exit_btn.png').convert_alpha()
        super().__init__(x, y, img, callback, scale)

# RestartButton is a specialized Button with a predefined restart button image
class RestartButton(Button):
    """
    A specialized Button class for the restart button, using a predefined image.
    """

    def __init__(self, x, y, callback, scale = 1):
        """
        Initialize the RestartButton with its own image and callback.
        :param x: The x-coordinate for the button's top-left corner.
        :param y: The y-coordinate for the button's top-left corner.
        :param callback: The function to call when the button is clicked.
        :param scale: The scale factor to apply to the button's image (default is 1).
        """
        img = pygame.image.load('img/restart_btn.png').convert_alpha()
        super().__init__(x, y, img, callback, scale)
