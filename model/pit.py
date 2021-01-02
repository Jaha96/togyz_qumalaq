from model.player import PlayerColor

class Pit():
    
    def __init__(self, player_color:PlayerColor, pit_index, seed_count, is_tuzdik=False):
        """
        Parameters
        ----------
        player_index : PlayerColor
            NOTE index of the player. 0 is top, 1 is bottom
        pit_index : int
            Index of the pit 1-9
        seed_count : int
            Total seed count in a current pit
        is_tuzdik : bool
            type of the current seed
        """
        self.player_color = player_color
        self.pit_index = pit_index
        self.seed_count = seed_count
        self.is_tuzdik = is_tuzdik
    