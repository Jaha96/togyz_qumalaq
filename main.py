from controller.game_controller import GameController

if __name__ == "__main__":

    controller = GameController()
    while True:
        controller.state.print_board()
        controller.print_possible_actions()
        possible_actions = controller.state.get_possible_action_player()
        selection = int(input('Select action: '))
        selected_action = possible_actions[selection]
        print("Selected action: ", selected_action)
        controller.result_function(selected_action)
        for player in controller.state.board.player_list:
            print(player.color, ": ", player.score, end=", ")
    
    # state = controller.state
    # while True:
    #     selection = int(input('Select action for '+possible_actions["actor"]+': '))
    #     selected_action = list(possible_actions["action"].values())[selection]
    #     print("Selected action: ", selected_action)
    #     state = controller.result_function(state, selected_action)
    #     state.print_board()
    #     possible_actions = get_possible_actions(state)


    