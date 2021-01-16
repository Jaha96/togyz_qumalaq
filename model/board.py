from model.pit import Pit
from model.player import Player, PlayerColor
from copy import deepcopy

class Move():
    def __init__(self, player_color, pit_index, action, kazan_point, opponent_kazan_point, advantage_seed_count, miss_seed_count):
        self.player_color = player_color
        self.pit_index = pit_index
        # NOTE might be added target pit_index
        self.action = action
        self.kazan_point = kazan_point
        self.opponent_kazan_point = opponent_kazan_point
        self.advantage_seed_count = advantage_seed_count
        self.miss_seed_count = miss_seed_count
    
    def __str__(self):
        return str(self.player_color) +" "+ str(self.pit_index) +" "+ self.action +" "+ str(self.kazan_point) +" "+ str(self.opponent_kazan_point) +" "+ str(self.advantage_seed_count) +" "+ str(self.miss_seed_count)

class Board():

    def __init__(self):
        self.PIT_SIZE = 9
        self.SEED_COUNT = 9
        self.player_list = []
        self.player_list.append(Player(PlayerColor.TOP))
        self.player_list.append(Player(PlayerColor.BOTTOM))

        for player in self.player_list:
            for pit_index in range(self.PIT_SIZE):
                player.pits.append(Pit(player.color, pit_index+1, self.SEED_COUNT, False))
    
    def get_opponent_player(self, current_player_color: PlayerColor):
        index = self.get_opponent_player_index(current_player_color)
        return self.player_list[index]

    def get_opponent_player_index(self, current_player_color: PlayerColor):
        if current_player_color == PlayerColor.BOTTOM:
            return self.get_player_index_by_color(PlayerColor.TOP)
        else:
            return self.get_player_index_by_color(PlayerColor.BOTTOM)

    def get_player_by_color(self, player_color: PlayerColor):
        return self.player_list[self.get_player_index_by_color(player_color)]

    def get_player_index_by_color(self, player_color: PlayerColor):
        return [i for i, e in enumerate(self.player_list) if e.color == player_color][0]

    def print_board(self):
        line_count = 100
        print("-"*line_count)

        top_player = self.get_player_by_color(PlayerColor.TOP)
        bottom_player = self.get_player_by_color(PlayerColor.BOTTOM)

        top_player_ordered = [None for i in range(9)]
        for pit in top_player.pits:
            new_index =self.PIT_SIZE - pit.pit_index
            top_player_ordered[new_index] = pit
        
        for pit in top_player_ordered:
            if pit.is_tuzdik:
                print("[{}]: {}".format(str(pit.pit_index), "Tuz"),end =" ")
            else:
                print("[{}]: {}".format(str(pit.pit_index), str(pit.seed_count)),end =" ")

        print("\n\n")
        for pit in bottom_player.pits:
            if pit.is_tuzdik:
                print("[{}]: {}".format(str(pit.pit_index), "Tuz"),end =" ")
            else:
                print("[{}]: {}".format(str(pit.pit_index), str(pit.seed_count)),end =" ")
        
        del top_player_ordered
        del top_player
        del bottom_player
        print()


        print("-"*line_count)
    
    def get_opponent_index(self, index: int):
        if index == 1:
            return 0
        elif index == 0:
            return 1

    def complete_action(self, action: Move):
        
        player_index = self.get_player_index_by_color(action.player_color)
        opponent_index = self.get_opponent_index(player_index)

        pit_index = action.pit_index - 1
        pit = self.player_list[player_index].pits[pit_index]
        color_index = player_index
        
        kazan_point = 0
        opponent_kazan_point = 0
        advantage_seed_count = 0
        miss_seed_count = 0

        temp_seed_count = self.player_list[color_index].pits[pit_index].seed_count
        self.player_list[color_index].pits[pit_index].seed_count = 0

        if temp_seed_count == 1:
            if pit_index >= (self.PIT_SIZE - 1):
                color_index = self.get_opponent_index(color_index)
                pit_index = 0
            else:
                pit_index += 1
        for seed in range(temp_seed_count):
            if player_index == color_index:
                # plus
                if self.player_list[color_index].pits[pit_index].is_tuzdik:
                    opponent_kazan_point += 1
                else:
                    advantage_seed_count += 1
                    self.player_list[color_index].pits[pit_index].seed_count += 1
            else:
                # opponent side minus
                if self.player_list[color_index].pits[pit_index].is_tuzdik:
                    kazan_point += 1
                elif (seed + 1) == temp_seed_count:
                    # last one
                    self.player_list[color_index].pits[pit_index].seed_count += 1
                    if self.player_list[color_index].pits[pit_index].seed_count % 2 == 0:
                        kazan_point += self.player_list[color_index].pits[pit_index].seed_count
                        self.player_list[color_index].pits[pit_index].seed_count = 0
                    elif is_tuzdik_possible(self, color_index, player_index, pit_index):
                        action = "tuzdik"
                        kazan_point += self.player_list[color_index].pits[pit_index].seed_count
                        self.player_list[color_index].pits[pit_index].seed_count = 0
                        self.player_list[color_index].pits[pit_index].is_tuzdik = True
                        self.player_list[player_index].tuzdik = True
                    else:
                        miss_seed_count += 1
                else:
                    miss_seed_count += 1
                    self.player_list[color_index].pits[pit_index].seed_count += 1

            if pit_index >= (self.PIT_SIZE - 1):
                color_index = self.get_opponent_index(color_index)
                pit_index = 0
            else:
                pit_index += 1
        
        self.player_list[player_index].score += kazan_point
        self.player_list[opponent_index].score += opponent_kazan_point

        return self

    


    def possible_move(self,player_color: PlayerColor):
        """
        Get possible move of the players.
        ...
        Parameters
        ----------
        list_pawn : list
            list of possible moves
        """
        list_possible_move = []
        orig_board = deepcopy(self)
        

        player = orig_board.get_player_by_color(player_color)
        for pit in player.pits:
            if pit.seed_count == 0 or pit.is_tuzdik:
                continue
            
            action = "move"
            kazan_point = 0
            opponent_kazan_point = 0
            advantage_seed_count = 0
            miss_seed_count = 0

            temp_board = deepcopy(orig_board)
            player_index = temp_board.get_player_index_by_color(player_color)
            pit_index = pit.pit_index - 1
            color_index = player_index
            
            temp_seed_count = temp_board.player_list[color_index].pits[pit_index].seed_count
            temp_board.player_list[color_index].pits[pit_index].seed_count = 0

            if temp_seed_count == 1:
                if pit_index >= (self.PIT_SIZE - 1):
                    color_index = temp_board.get_opponent_index(color_index)
                    pit_index = 0
                else:
                    pit_index += 1
            for seed in range(temp_seed_count):
                if player_index == color_index:
                    # plus
                    if temp_board.player_list[color_index].pits[pit_index].is_tuzdik:
                        opponent_kazan_point += 1
                    else:
                        advantage_seed_count += 1
                        temp_board.player_list[color_index].pits[pit_index].seed_count += 1
                else:
                    # opponent side minus
                    if temp_board.player_list[color_index].pits[pit_index].is_tuzdik:
                        kazan_point += 1
                    elif (seed + 1) == temp_seed_count:
                        # last one
                        temp_board.player_list[color_index].pits[pit_index].seed_count += 1
                        if temp_board.player_list[color_index].pits[pit_index].seed_count % 2 == 0:
                            kazan_point += temp_board.player_list[color_index].pits[pit_index].seed_count
                            temp_board.player_list[color_index].pits[pit_index].seed_count = 0
                        elif is_tuzdik_possible(temp_board, color_index, player_index, pit_index):
                            action = "tuzdik"
                            kazan_point += temp_board.player_list[color_index].pits[pit_index].seed_count
                            temp_board.player_list[color_index].pits[pit_index].seed_count = 0
                            temp_board.player_list[color_index].pits[pit_index].is_tuzdik = True
                            temp_board.player_list[player_index].tuzdik = True
                        else:
                            miss_seed_count += 1
                    else:
                        miss_seed_count += 1
                        temp_board.player_list[color_index].pits[pit_index].seed_count += 1

                if pit_index >= (temp_board.PIT_SIZE - 1):
                    color_index = temp_board.get_opponent_index(color_index)
                    pit_index = 0
                else:
                    pit_index += 1
            
            action, kazan_point = check_and_complete_atsurau(temp_board, player, action, kazan_point)

            move = Move(player_color, pit.pit_index, action, kazan_point, opponent_kazan_point, advantage_seed_count, miss_seed_count)
            list_possible_move.append(move)

        return list_possible_move

def check_and_complete_atsurau(board: Board, player: Player, action, kazan_point):
        opponent_player = board.get_player_by_color(player.enemy_color)
        player_index = board.get_player_index_by_color(player.color)
        opponent_seed_count = 0
        for o_pit in opponent_player.pits:
            opponent_seed_count += o_pit.seed_count

        # Opponent has no more moves, In this case execute atsurau
        if opponent_seed_count == 0:
            action = "atsurau"
            for pit in player.pits:
                kazan_point += pit.seed_count
                board.player_list[player_index].pits[pit.pit_index - 1].seed_count = 0
            
        return action, kazan_point

def is_tuzdik_possible(board: Board, opponent_index, player_index, pit_index):
        seed_count = board.player_list[opponent_index].pits[pit_index].seed_count
        pits = board.player_list[opponent_index].pits
        tuzdik = board.player_list[player_index].tuzdik
        opponent_tuzdik_index = -1
        for pit in board.player_list[player_index].pits:
            if pit.is_tuzdik == True:
                opponent_tuzdik_index = pit.pit_index
        pit_number = pit_index + 1
        if seed_count == 3 and pit_number != 9 and tuzdik == False and pit_number != opponent_tuzdik_index:
            return True
        return False