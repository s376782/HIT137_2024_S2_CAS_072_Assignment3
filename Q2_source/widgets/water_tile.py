from widgets.tile import Tile

class WaterTile(Tile):
    """
    WaterTile is a subclass of Tile that represents a specific type of tile in the game, namely a water tile.
    It inherits all properties and behavior from the Tile class, but can be extended to include
    water-specific behaviors in the future (e.g., animations, effects, or interactions with the player).
    """

    def __init__(self, tile, x, y):
        super().__init__(tile, x, y)