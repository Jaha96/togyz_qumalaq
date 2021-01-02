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

    # Deprecated move function
    def move(self, action: Move):
        """
        Function of action "move"
        Parameters
        ----------
        pawn_index : int
            the pawn index in the list
        player_color : int
            player's color or index in the list
        """
        player = self.player_list[player_color]
        player_board = self.board[player.color]
        enemy_board = self.board[player.enemy_color]
        current_pit_seeds = player_board[pit_index]

        # Current moving pit will be 1, loop starts from next pit
        self.board[player.color][pit_index] = 1
        current_pit_seeds -= 1
        current_pit_index = pit_index

        board_row_index = player.color
        for seed in range(current_pit_seeds):
            if self.is_last_seed(self.board[board_row_index], current_pit_index):
                current_pit_index = 0
                board_row_index = 1 if player.color == 0 else 0
            else:
                current_pit_index += 1
            self.board[board_row_index][current_pit_index] += 1
        
        if board_row_index != player.color:
            last_pit_seed = self.board[board_row_index][current_pit_index]
            if last_pit_seed % 2 == 0:
                self.board[board_row_index][current_pit_index] = 0
                self.player_list[player_color].score += last_pit_seed

    