import time
import os
import random
import math
import animate
import credits


def clscreen():
    '''cls/clear function'''
    os.system('cls' if os.name == 'nt' else 'clear')


def init_board():
    """Returns an empty 3-by-3 board (with .). Not anymore, it'll look cleaner like this I think."""
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    return board


def get_move(board):
    '''asks player for move, checks validity'''
    while True:
        player_move = input(
            "Select a valid field from columns A to C and rows 1 to 3\n")
        if player_move.lower() == 'quit':
            quit()
        move_check = [field for field in player_move]
        if len(move_check) >= 2 and move_check[0] in ['1', '2', '3']:
            move_check = [move_check[1], move_check[0]]

        column, row = 0, 0
        if is_move_valid(move_check):
            column, row = convert_move_to_number(move_check)
            if not is_field_occupied(board, column, row):
                break
            else:
                clscreen()
                print_board(board, False)
                print("Field is already occupied.")
        else:
            clscreen()
            print_board(board, False)
            print("Invalid move.")
    return column, row


def convert_move_to_number(move):
    '''converts move from coordinates to numbers'''
    column, row = 0, 0
    check_column = ['a', 'b', 'c']
    check_row = ['3', '2', '1']
    for i in range(len(check_column)):
        if move[0].lower() == check_column[i]:
            column = i
    for i in range(len(check_row)):
        if move[1] == check_row[i]:
            row = i
    return column, row


def is_move_valid(move_check):
    '''checks if a move is valid'''
    return True if len(move_check) == 2 and move_check[0].lower() in ['a', 'b', 'c'] and\
        move_check[1] in ['1', '2', '3'] else False


def is_field_occupied(board, column, row):
    '''checks if field is filled'''
    return True if board[row][column] != '' else False


def mark(board, player, row, column):
    '''marks a field selected by player'''
    board[row][column] = player


def get_bot_move(board, bot_intelligence, current_player):
    '''bot move depending on selected AI'''
    if bot_intelligence == 1:
        return bot_random(board)
    if bot_intelligence == 2:
        return bot_smart(board, current_player)
    if bot_intelligence == 3:
        return bot_impossible(board, current_player)


def bot_random(board):
    '''dumb random bot'''
    possible_moves = get_possible_moves(board)
    row, column = random.choice(possible_moves)
    return row, column


def bot_smart(board, current_player):
    '''smarter bot function'''
    possible_moves = get_possible_moves(board)
    defending_row = -1
    defending_column = -1
    for row in range(3):
        for column in range(3):
            if not is_field_occupied(board, column, row):
                for i in range(2):
                    board[row][column] = i
                    if did_game_finish(board) and int(current_player) == i:
                        board[row][column] = ''
                        return row, column
                    elif did_game_finish(board) and int(current_player) != i:
                        defending_row, defending_column = row, column
                    board[row][column] = ''
    if defending_row != -1 and defending_column != -1:
        return defending_row, defending_column
    row, column = random.choice(possible_moves)
    return row, column


def bot_impossible(board, current_player):
    '''impossible bot function'''
    best_score = -math.inf
    best_move = ()
    for row in range(3):
        for column in range(3):
            if board[row][column] == '':
                mark(board, current_player, row, column)
                score = minimax(board, 0, False, current_player)
                board[row][column] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, column)
                pass
    row, column = best_move
    return row, column


def minimax(board, depth, is_maximizing, current_player):
    '''minimax algorithm for the impossible bot'''
    scores = {current_player: 1, not current_player: -1, 'tie': 0}
    winner = win_check(board)
    if winner != -1:
        return scores[winner]
    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for column in range(3):
                if board[row][column] == '':
                    board[row][column] = 1
                    score = minimax(board, depth + 1, False, current_player)
                    board[row][column] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for column in range(3):
                if board[row][column] == '':
                    board[row][column] = 0
                    score = minimax(board, depth + 1, True, current_player)
                    board[row][column] = ''
                    best_score = min(score, best_score)
        return best_score


def get_possible_moves(board):
    '''possible moves for the bot to make'''
    possible_moves = []
    for row in range(3):
        for column in range(3):
            if board[row][column] == '':
                possible_moves.append([row, column])
    return possible_moves


def win_check(board):
    """Returns True if player has won the game."""
    winner = -1

    for row in board:
        if row[0] == row[1] == row[2] != '':
            winner = row[0]

    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] != '':
            winner = board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != '':
        winner = board[1][1]
    if board[2][0] == board[1][1] == board[0][2] != '':
        winner = board[1][1]

    if winner == -1 and is_board_full(board):
        return 'tie'
    else:
        return winner


def did_game_finish(board):
    '''check if someone won'''
    return True if check_columns_for_win(board) or check_rows_for_win(board) or check_diagonals_for_win(board)\
        else False


def check_if_tie(board):
    '''check if the game finished with a tie'''
    if is_board_full(board):
        return True
    else:
        return False


def check_columns_for_win(board):
    '''checks if columns match and are not empty'''
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return True, row[0]
    return False


def check_rows_for_win(board):
    '''checks if rows match and are not empty'''
    for i in range(len(board)):
        if board[0][i] == board[1][i] == board[2][i] != '':
            return True, board[0][i]
    return False


def check_diagonals_for_win(board):
    '''checks if the diagonals match and are not empty'''
    if board[0][0] == board[1][1] == board[2][2] != '':
        return True, board[1][1]
    elif board[2][0] == board[1][1] == board[0][2] != '':
        return True, board[1][1]
    else:
        return False


def is_board_full(board):
    '''scans the board to check if it's full'''
    blank_count = 0
    for row in board:
        for field in row:
            if field == "":
                blank_count += 1
    if blank_count == 0:
        return True
    else:
        return False


def current_symbol(current_player):
    '''returns symbol based on player'''
    if current_player == 0:
        return "X"
    elif current_player == 1:
        return "O"
    else:
        raise ValueError("incorrect player")


def print_board(board, display_animation):
    '''prints the current board state'''
    visual_table = get_board_visual_table(board)
    out = """  +---+---+---+
3 | {0} | {1} | {2} |
  +---+---+---+
2 | {3} | {4} | {5} |
  +---+---+---+
1 | {6} | {7} | {8} |
  +---+---+---+
    A   B   C   """.format(*visual_table)

    if display_animation:
        animate.anim_init(out)
        animate.animate()
    else:
        print(out)


def get_board_visual_table(board):
    '''converts fields from the board to Os, Xs and whitespaces'''
    visual_board = []
    for row in board:
        for field in row:
            if field == 0:
                visual_board.append('X')
            elif field == 1:
                visual_board.append('O')
            else:
                visual_board.append(' ')
    return visual_board


def print_result(current_player, did_someone_win):
    """Congratulates winner or proclaims tie (if winner equals zero)."""
    if did_someone_win is True:
        print("Player ", int(current_player)+1, " (",
              current_symbol(int(current_player)), ") has won the match!", sep='')
        time.sleep(5)
    else:
        print("This is a tie!")
        time.sleep(5)


def compare_player_type(current_player, player_1_type, player_2_type):
    '''check if current player should be an AI'''
    if current_player == 0 and player_1_type == 1:
        return True
    elif current_player == 0 and player_1_type == 2:
        return False
    if current_player == 1 and player_2_type == 1:
        return True
    elif current_player == 1 and player_2_type == 2:
        return False


def tictactoe_game(player_1_type, player_2_type, bot_intelligence):
    '''Main game function'''
    clscreen()
    board = init_board()
    current_player = 0
    did_someone_win = False
    # use get_move(), mark(), has_won(), is_full(), and print_board() to create game logic

    start = True
    while not is_board_full(board):
        clscreen()
        print_board(board, start)
        start = False

        if compare_player_type(current_player, player_1_type, player_2_type):
            column, row = get_move(board)
            mark(board, current_player, row, column)
        else:
            time.sleep(1)
            row, column = get_bot_move(board, bot_intelligence, current_player)
            mark(board, current_player, row, column)
        if did_game_finish(board) is True:
            did_someone_win = True
            break
        current_player = not current_player
    clscreen()
    print_board(board, False)
    print_result(current_player, did_someone_win)


def main_menu():
    '''menu of the game'''
    bot_intelligence_list = ['Random', 'Smart', 'Impossible']
    bot_intelligence = 1
    while True:
        clscreen()
        print("Welcome to Tic-Tac-Toe!\nType the number next to the mode to select the mode, or type"
              " 'quit' to exit the program!\nCurrently selected Computer intelligence:",
              bot_intelligence_list[bot_intelligence-1])
        user_input = input(
            "1. Player vs Player\n2. Player vs Computer\n3. Computer vs Computer\n4. "
            "Select Computer player intelligence\n5. Credits\n")
        if user_input == '1':
            tictactoe_game(1, 1, bot_intelligence)
        elif user_input == '2':
            tictactoe_game(1, 2, bot_intelligence)
        elif user_input == '3':
            tictactoe_game(2, 2, bot_intelligence)
        elif user_input == '4':
            bot_intelligence = bot_intelligence_select_menu()
        elif user_input == '5':
            credits.show_credits()
            input("Press enter to continue")
        elif user_input == 'quit':
            quit()


def bot_intelligence_select_menu():
    '''select smarts of the bot'''
    while True:
        clscreen()
        print("Hello! Choose a bot difficulty. Unlisted keys will return to main menu.")
        user_input = input("1. Random\n2. Smarter\n3. Impossible\n")
        if user_input == '1':
            return 1
        elif user_input == '2':
            return 2
        elif user_input == '3':
            return 3


if __name__ == '__main__':
    main_menu()
