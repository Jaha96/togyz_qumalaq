from model.state import State
from model.player import PlayerColor
from copy import deepcopy
from model.board import Move
class AIElements:

    def get_possible_action(state: State):
        all_possible_action = state.get_possible_action_player()
        return all_possible_action
    
    def result_function(state: State, action: Move): 
        new_state  = deepcopy(state)
        new_state.complete_action(action)
        new_state.change_turn()
        return new_state

    def evaluation_function(state: State, player_color: PlayerColor):
        player = state.board.get_player_by_color(player_color)
        return player.score