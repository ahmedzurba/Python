# Author  : Ahmed Zurba
# Python 3.10
import random




def game_initialization():
    board_size = input("Please enter field size: ")
    min_board_size = 3

    abc_list = list(map(chr, range(65, 91)))  # size of 26
    abc_to_append_list = list(map(chr, range(65, 91)))

    while (not board_size.isdigit()) or (int(board_size) < min_board_size):
        board_size = input("Please enter field size, only numbers larger than 3: ")
    board_size = int(board_size)

    # if the abc list shorter than game size, adds another abc list (each time the letters double themselves)
    # to the end of the list until desired size is reached
    if len(abc_list) < board_size:
        times_bigger = int(board_size / len(abc_list)) + (
                    board_size % len(abc_list) > 0)  # rounded up
        for i in range(1, times_bigger):  # every iteration add a list of new alphabetic aa bb .. aaa bbb ..
            combine = list(zip(abc_list, abc_to_append_list))
            abc_to_append_list = [item[0] + item[1] for item in combine]
            abc_list.extend(abc_to_append_list)
    table_name = abc_list[:board_size]  # cuts the list of table names acc. to size
    table_dict = dict.fromkeys([i for i in range(1, board_size ** 2 + 1)], "")
    game_field = {chars: table_dict.copy() for chars in table_name}
    return game_field


def is_winner(game_field, player_type):
    united_X_O_set = set()
    same_nested_keys_list = []
    possible_wins_lists_list = []
    boards_full = True  # boolean var to check if game is over due to draw - no unfilled places left on any boards
    did_win_united_board = False  # bool var to check if won game due to pattern match on the merged board
    board_size = len(game_field)
    # possible win patterns, in a list, appended to a list of all win patterns
    # i=0..(board_size -1)   row_or_col=1..board_size
    # First diagonal 1 to board size: 1+i*(board_size + 1)
    possible_wins_lists_list.append([(1 + i * (board_size + 1)) for i in range(board_size)])
    # Second diagonal: board_size + i*(board_size-1)
    possible_wins_lists_list.append([(board_size + i * (board_size - 1)) for i in range(board_size)])
    for row_or_col in range(1, board_size + 1):
        # Vertical: creates a list of lists - list of all possible matching vertical col. indices: row_or_col+i * board_size
        possible_wins_lists_list.append([(row_or_col + i * board_size) for i in range(board_size)])
        # Horizontal: same as vertical, but for horizontal matches: (row_or_col-1)*board_size+1+i
        possible_wins_lists_list.append([((row_or_col - 1) * board_size + 1 + i) for i in range(board_size)])
    for table_num, table_contents in game_field.items():
        player_type_indices = list(key for (key, value) in table_contents.items() if value == player_type)
        player_taken_indices = list(key for (key, value) in table_contents.items() if value != '')
        boards_full = True if (boards_full and len(player_taken_indices) == (board_size ** 2)) else False
        if same_nested_keys_list == []:  # insert first list of X indices if this is the first table
            same_nested_keys_list = player_type_indices.copy()
        else:  # otherwise-check for every value in same_nested.. if it exists in player_type_indices, only then keep it
            same_nested_keys_list = [type_index for type_index in same_nested_keys_list \
                                     if type_index in player_type_indices]
        united_X_O_set.update(
            player_type_indices)  # Unites all tables in one with the placements of the needed player type
    united_X_O_list = list(united_X_O_set)
    for i in range(len(possible_wins_lists_list)):
        did_win_united_board = (
                did_win_united_board or all(item in united_X_O_list for item in possible_wins_lists_list[i]))
    if (
            same_nested_keys_list != [] or did_win_united_board):  # returns 2 if won - same player_type(X/O) in same place on all boards, all reg. match on united board
        print("Congratulations! You have won this game!")
        return 2
    elif (boards_full):
        print("It's a draw!")
        return 1
    else:
        return 0


def is_possible(coords, game_dic):
    if game_dic[(coords).split()[0]][int(coords.split()[1])] == "":
        return True
    else:
        print("Already occupied")
        return False


def correct_input_num_N(coords, game_dic):
    n = len(game_dic)
    new_n = n % 26
    max = n ** 2
    max_number = len(str(max))
    chars_count = n // 26 + 1

    if len(coords.split()) != 2:
        return False
    chars = coords.split()[0]
    digits = coords.split()[1]
    if 3 <= len(coords) <= chars_count + max_number + 1:
        if chars.isalpha() and digits.isdigit():
            chars = chars.upper()
            if 0 < int(digits) <= max:
                if len(chars) == chars_count:
                    if (chars[-1] in list(map(chr, range(65, 65 + new_n)))):
                        for c in chars:
                            if c != chars[-1]:
                                return False
                        return is_possible(coords, game_dic)
                else:
                    if (chars[-1] in list(map(chr, range(65, 91)))):
                        for c in chars:
                            print(c)
                            if c != chars[-1]:
                                return False
                        return is_possible(coords, game_dic)
    return False


def player_names():
    players_names_list = []
    players_number = 2
    for i in range(players_number):
        players_names_list.append(input("Please enter your name: "))
    random.shuffle(players_names_list)
    print(f'{players_names_list[0]} plays first with X, {players_names_list[1]} plays second with O')
    return players_names_list


def change_player(current_player, player_x, player_o):
    if current_player == player_x:
        return ("O", player_o)
    else:
        return ("X", player_x)


def draw_game(game_field):
    n = len(game_field)
    index = 1

    for i in game_field:
        print(f" (Board {i})  ")
        for v in game_field[i].values():
            if v == "":
                v = " "
            if index in [n * ind for ind in range(1, n + 1)]: #last index in every line
                print(f" {v} ", end="")
                print("\n" + "---+" * n)
                index += 1
            else:
                print(f" {v} ", end="|")
                index += 1
            if index > n ** 2:
                index = 1
                print()


def start_game():

    player_list = player_names()
    #start new game after game over
    #random
    player_x = player_list[0]
    player_o = player_list[1]
    current_player = player_x
    used_char = "X"

    game_dic = game_initialization()
    while True:
        coords = input(f'{current_player} please enter number from [a,b,c] [1-9] if possible : ')
        while not correct_input_num_N(coords, game_dic):
            coords = input(f'{current_player} please enter number from [a,b,c] [1-9] if possible : ')

        game_dic[coords.split()[0]][int(coords.split()[1])] = used_char
        draw_game(game_dic)
        if is_winner(game_dic, used_char):
            print(current_player, "winner!!")
            break
        used_char, current_player = change_player(current_player, player_x, player_o)


def highscore(winner_array, winner):
    if winner == "x":
        winner_array["x"] += 2
    elif winner == "o":
        winner_array["o"] += 2
    else:
        winner_array["x"] += 1
        winner_array["o"] += 1


if __name__ == '__main__':
    start_game()
