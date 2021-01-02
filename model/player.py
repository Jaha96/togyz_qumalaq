from enum import Enum

class PlayerColor(Enum):
    TOP = 0
    BOTTOM = 1

    def __str__(self):
        return "Player "+self.name

class Player():
    """
        A model class used to represent the player.
        Color 0 for white and 1 for black
    """
    def __init__(self, color:PlayerColor):
        """
        Parameters
        ----------
        color : int
            Player index. 0 = white, 1 = black
        """
        self.color = color
        self.enemy_color = PlayerColor.BOTTOM if color == PlayerColor.TOP else PlayerColor.TOP
        self.score = 0
        self.tuzdik = False
        self.pits = []
    