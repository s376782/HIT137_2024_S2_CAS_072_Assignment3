from widgets.tile import Tile

class ExitTile(Tile):
    """
    ExitTile is a subclass of Tile that represents the exit point in a game level.
    When the player reaches this tile, the level is considered complete.
    """

    def __init__(self, tile, x, y):
        """
        Initialize the ExitTile object.
        :param tile: Index of the tile image used for the exit.
        :param x: The x-coordinate where the exit tile is placed.
        :param y: The y-coordinate where the exit tile is placed.
        """
        super().__init__(tile, x, y)