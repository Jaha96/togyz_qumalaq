from model.state import State
from model.player import PlayerColor
from copy import deepcopy

class GameController():
    def __init__(self):
        starter = PlayerColor.BOTTOM
        self.state = State(starter)
        self.state.initial_state()
        self.possible_action_keys = []
        self.two_players = False
        self.player_vs_ai_white = False
    
    def print_possible_actions(self):
        all_possible_action = self.state.get_possible_action_player()
        index = 0

        print("player_color, pit_index, action, kazan_p, opponent_k_p, a_seed_count, m_seed_count")
        for move in all_possible_action:
            print(index, move)
            index += 1
        return all_possible_action

    def result_function(self,state,action): 
        new_state = deepcopy(state)

        if action['action'] == 'tuzdik':
            pit_index = action['pit_index']
            player_color = action['player_index']
            new_state.activate_tuzdik(pit_index, player_color)

        if action['action'] == 'move':
            pit_index = action['pit_index']
            player_color = action['player_index']
            new_state.move(pit_index, player_color)
        new_state.change_turn()
        return new_state