from model.state import State
from model.player import PlayerColor
from copy import deepcopy
from ai_modules.classic_algorithm import MinimaxAgent

class GameController():
    def __init__(self):
        starter = PlayerColor.BOTTOM
        self.state = State(starter)
        self.state.initial_state()
        self.possible_action_keys = []
        self.two_players = False
        self.player_vs_ai_white = False
        self.ai_agent = MinimaxAgent(4, PlayerColor.TOP)
    
    def print_possible_actions(self):
        all_possible_action = self.state.get_possible_action_player()
        index = 0

        print("kazan_p, opponent_k_p, a_seed_count, m_seed_count")
        for move in all_possible_action:
            print(index, move)
            index += 1
        return all_possible_action
