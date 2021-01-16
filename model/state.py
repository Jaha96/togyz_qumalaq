# from model.player import Player
from model.board import Board, Move
from model.player import PlayerColor

import random
# import pandas as pd
from copy import deepcopy

class State:
    def __init__(self, starter:PlayerColor):
        self.turn = 1
        self.starter = starter
        self.board = []
        self.history = []

    def initial_state(self):
        self.board = Board()

    def get_player_index(self):
        if self.starter == PlayerColor.BOTTOM:
            if self.turn % 2 == 0:
                return self.board.get_player_index_by_color(PlayerColor.TOP)
            else:
                return self.board.get_player_index_by_color(PlayerColor.BOTTOM)
        else:
            if self.turn % 2 == 0:
                return self.board.get_player_index_by_color(PlayerColor.BOTTOM)
            else:
                return self.board.get_player_index_by_color(PlayerColor.TOP)
    
    def print_board(self):
        self.board.print_board()

    def get_possible_action_player(self):
        player = self.board.player_list[self.get_player_index()]
        p_moves = self.board.possible_move(player.color)
        return p_moves

    def change_turn(self):
        """
        Add effect on changing the turn
        """
        self.turn += 1
        # new_state = deepcopy(self)
        # self.history.append(new_state)
        # del new_state

    def is_last_seed(self, player_board, pit_index):
        last_index = len(player_board) - 1
        if pit_index == last_index:
            return True
        return False
    
    def complete_action(self, action: Move):
        return self.board.complete_action(action)
    
    def is_terminal(self):
        top_player = self.board.get_player_by_color(PlayerColor.TOP)
        bottom_player = self.board.get_player_by_color(PlayerColor.BOTTOM)

        if top_player.score > 81 or bottom_player.score > 81:
            return True
        
        if top_player.score == 81 and bottom_player.score == 81:
            return True

        return False
    
    def get_winner(self, player_color: PlayerColor):
        player = self.board.get_player_by_color(player_color)
        if player.score > 81:
            return True
        if player.score == 81:
            return True
