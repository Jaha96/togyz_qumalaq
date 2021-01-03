from controller.game_controller import GameController
from ai_modules.ai_elements import AIElements

if __name__ == "__main__":

    controller = GameController()
    i = 0
    while True:
        controller.state.print_board()
        if controller.state.is_terminal():
            print("\n\nGAME OVER\n\n")
            break
        if i % 2 == 0:
            controller.print_possible_actions()
            possible_actions = controller.state.get_possible_action_player()
            selection = int(input('Select action: '))
            selected_action = possible_actions[selection]
        else:
            score, selected_action = controller.ai_agent.choose_action(controller.state)

        print("Selected action: ", selected_action)
        controller.state = AIElements.result_function(controller.state, selected_action)
        for player in controller.state.board.player_list:
            print(player.color, ": ", player.score, end=", ")
        i+= 1
    