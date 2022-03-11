import copy
import random
import sys

EMPTY_FIELD = '_'
PLAYER_X = 'X'
PLAYER_AI = 'O'
BOARD_SIZE = 3
GAMES_COUNT = 100



def generate_board(size=BOARD_SIZE):
    '''
    Generate game board with BOARD_SIZE x BOARD_SIZE dimensions
    '''

    matrix = []
    for _ in range(size):
        matrix.append([EMPTY_FIELD for __ in range(size)])
    return matrix



def is_valid_move():
    '''
    Check if the coordinates from user input are type: int, and in
    range BOARD_SIZE otherwise print message with a problem description
    and call again the function until the input contains only correct
    values
    '''
    try:
        row, col = [int(x) for x in input().split()]

        if not ((0 <= row < BOARD_SIZE) and (0 <= col < BOARD_SIZE)):
            print('This is not a valid move!\n'
                  'Every valid move contains 2 numbers, seperated by space in range(0, 2)\n'
                  'Enter yor move again:')
            return is_valid_move()
        return row, col
    except ValueError or IndexError:
        print('Enter two valid numbers separated by space!')
        return is_valid_move()


def check_is_free_field(r, c, data):
    '''
    Check if the chosen field is not already filled.
    '''
    try:
        if not data[r][c] == '_':
            print(f'The field with coordinates ({r}, {c}) is not free!')
            return False
        return True
    except IndexError:
        print('Please, enter 2 numbers, seperated by space in range(0, 2)')
        return


def check_sequence(seq):
    '''
    check if the given sequence contains only equal elements
    different from EMPTY_FIELD
    '''
    if seq[0] == EMPTY_FIELD:
        return EMPTY_FIELD
    if all([seq[0] == elem for elem in seq[1:]]):
        return seq[0]

    return EMPTY_FIELD


def check_rows(data):
    '''
    Check if every row contains only equal elements different
    from EMPTY_FIELD
    '''
    for row in data:
        check = check_sequence(row)
        if check != EMPTY_FIELD:
            return check
    return EMPTY_FIELD


def check_columns(data):
    '''
    Check if every column contains only equal elements different
    from EMPTY_FIELD
    '''
    for col in range(BOARD_SIZE):
        columns = []
        for row in range(BOARD_SIZE):
            columns.append(data[row][col])
        check = check_sequence(columns)
        if check != EMPTY_FIELD:
            return check
    return EMPTY_FIELD


def check_primary_diagonal(data):
    '''
    Check if the primary diagonal contains only equal elements different
    from EMPTY_FIELD
    '''
    diagonal = []
    for i in range(BOARD_SIZE):
        diagonal.append(data[i][i])
    check = check_sequence(diagonal)
    if check != EMPTY_FIELD:
        return check
    return EMPTY_FIELD


def check_secondary_diagonal(data):
    '''
    Check if the secondary diagonal contains only equal elements different
    from EMPTY_FIELD
    '''
    diagonal = []
    for i in range(BOARD_SIZE):
        diagonal.append(data[i][BOARD_SIZE - i - 1])
    check = check_sequence(diagonal)
    if check != EMPTY_FIELD:
        return check
    return EMPTY_FIELD


def get_current_empty_fields(board):
    '''
    Collect and return all empty fields coordinates from the
    given board. If there not empty fields retun False
    '''
    empty_fields_coordinates = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY_FIELD:
                empty_fields_coordinates.append((row, col))
    if len(empty_fields_coordinates) > 0:
        return empty_fields_coordinates
    return False


def make_move(coordinates, player, board):
    '''
    Filled the given board field with the player's sign
    '''
    board[coordinates[0]][coordinates[1]] = player


def make_automatic_move(available_fields_list, game_board, player):
    '''
    Make a move with coordinates generated with random choice
    from free fields list
    '''
    coordinates = random.choice(available_fields_list)
    make_move(coordinates, player, game_board)


def change_player(current_player: bool):
    '''
    Return the opposite boolean value
    '''
    return not current_player


def pick_piece(current_player):
    '''
    Return the current player sign
    '''
    return PLAYER_X if current_player else PLAYER_AI


def get_score(score_board, board):
    '''
    Return the coordinates of the field with MAX score
    '''
    max_score = -sys.maxsize
    best_row = ''
    best_col = ''
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY_FIELD:
                if max_score < score_board[row][col]:
                    max_score = score_board[row][col]
                    best_row = row
                    best_col = col
    return best_row, best_col


def update_score_board(current_board, result_board, winner):
    '''
    Calculate the score board after win. The values are:
    +1 for the winner's fields
    -1 for the loser's fields.
    '''
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if current_board[row][col] == pick_piece(winner):
                result_board[row][col] += 1
            if current_board[row][col] == pick_piece(not winner):
                result_board[row][col] -= 1


def view_board_state(board):
    '''
    Print the current board
    '''
    for row in board:
        print(' '.join([str(x) for x in row]))
    print('\n')


def check_for_winner(data):
    '''
    Check every row, column and diagonal for winner.
    '''
    return not (check_rows(data) == check_columns(data) == check_primary_diagonal(data) ==
                check_secondary_diagonal(data) == EMPTY_FIELD)


def find_best_ai_move(board, current_player):
    '''
    Generate a board with scores which will help the AI to choose his
    next best move.
    The start position of every game will be always the given board.
    The score board will calculate his fields after every game with WIN.
    The count of AI played games depends on GAMES_COUNT. The best move for AI
    is the board field with max score.
    '''
    score_board = []
    for i in range(BOARD_SIZE):
        score_board.append([0, 0, 0])

    for _ in range(GAMES_COUNT):
        current_game_board = copy.deepcopy(board)

        while True:
            current_player = change_player(current_player)
            empty_fields_list = get_current_empty_fields(current_game_board)
            if empty_fields_list:
                coordinates = random.choice(empty_fields_list)
                make_move(coordinates, pick_piece(current_player), current_game_board)

                if check_for_winner(current_game_board):
                    update_score_board(current_game_board, score_board, current_player)
                    break

                if not get_current_empty_fields(current_game_board):
                    break

    best_score = get_score(score_board, board)
    # view_board_state(score_board)
    print(f'Best move for AI is {best_score}')

    return best_score


def main():
    '''
    Initialize a board, players and messages with information about the
    game state after every move. Changes the player and AI after every move.
    If there is a win or all of the board fields are filled, the game ends.
    '''

    game_board = generate_board()
    view_board_state(game_board)
    current_player = True

    while True:
        print('Enter your move in order row col:')
        coordinates = is_valid_move()

        while not check_is_free_field(coordinates[0], coordinates[1], game_board):
            print('Enter your move again:')
            coordinates = is_valid_move()

        make_move(coordinates, pick_piece(current_player), game_board)
        view_board_state(game_board)

        if check_for_winner(game_board):
            print(f'*** The WINNER is PLAYER ***')
            break

        if get_current_empty_fields(game_board):
            ai_coordinates = find_best_ai_move(game_board, pick_piece(current_player))
            make_move(ai_coordinates, PLAYER_AI, game_board)
            view_board_state(game_board)
            if check_for_winner(game_board):
                print(f'*** The WINNER is AI ***')
                break

        if not get_current_empty_fields(game_board):
            print(f'Game over! We don\'t have a winner!')
            break


if __name__ == '__main__':
    main()
