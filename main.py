from controller.game_controller import GameController

if __name__ == "__main__":

    controller = GameController()
    controller.state.print_board()
    controller.print_possible_actions()
    # possible_actions = get_possible_actions(controller.state)

    
    # state = controller.state
    # while True:
    #     selection = int(input('Select action for '+possible_actions["actor"]+': '))
    #     selected_action = list(possible_actions["action"].values())[selection]
    #     print("Selected action: ", selected_action)
    #     state = controller.result_function(state, selected_action)
    #     state.print_board()
    #     possible_actions = get_possible_actions(state)


    