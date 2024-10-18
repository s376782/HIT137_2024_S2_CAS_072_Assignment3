#https://github.com/s376782/HIT137_2024_S2_CAS_072_Assignment3/tree/main/Q2_source
from widgets.tile import Tile

class DecorationTile(Tile):
    """
    DecorationTile is a subclass of Tile that represents non-interactive decoration elements in the game.
    These tiles are purely visual and do not affect gameplay, such as background objects, trees, or rocks.
    """

    def __init__(self, tile, x, y):
        """
        Initialize the DecorationTile object.
        :param tile: Index of the tile image used for the decoration.
        :param x: The x-coordinate where the decoration tile is placed.
        :param y: The y-coordinate where the decoration tile is placed.
        """
        super().__init__(tile, x, y)