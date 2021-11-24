from random import shuffle
from model.player import PlayerColor
from model.state import State
from ai_modules.ai_elements import AIElements

class MinimaxAgent():

    def __init__(self, max_depth, player_color: PlayerColor):
        self.max_depth = max_depth
        self.player_color = player_color

    
    def choose_action(self, state: State):
        """
        Predict the move using minimax algorithm
        Parameters
        ----------
        state : State
        Returns
        -------
        float, int:
            The evaluation or utility and the action index
        """
        list_action = AIElements.get_possible_action(state)
        eval_score, selected_action_index = self._minimax(0,state,True,float('-inf'),float('inf'))
        return (eval_score,list_action[selected_action_index])
    
    def _minimax(self, current_depth, state, is_max_turn, alpha, beta):

        if current_depth == self.max_depth or state.is_terminal():
            return AIElements.evaluation_function(state, self.player_color), None

        possible_action = AIElements.get_possible_action(state)
        index_of_actions = [i for i, action in enumerate(possible_action)]

        shuffle(index_of_actions) #randomness
        best_value = float('-inf') if is_max_turn else float('inf')
        action_target = None
        for action_index in index_of_actions:
            new_state = AIElements.result_function(state,possible_action[action_index])

            eval_child, action_child = self._minimax(current_depth+1,new_state,not is_max_turn, alpha, beta)

            if is_max_turn and best_value < eval_child:
                best_value = eval_child
                action_target = action_index
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break

            elif (not is_max_turn) and best_value > eval_child:
                best_value = eval_child
                action_target = action_index
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, action_target
