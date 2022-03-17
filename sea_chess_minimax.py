import copy
import random
import sys

EMPTY_FIELD = '_'
PLAYER_X = 'X'
PLAYER_AI = 'O'
BOARD_SIZE = 3


def generate_board(size=BOARD_SIZE):
    """
    Generate game board with BOARD_SIZE x BOARD_SIZE dimensions
    """

    matrix = []
    for _ in range(size):
        matrix.append([EMPTY_FIELD for __ in range(size)])
    return matrix


def is_valid_move():
    """
    Check if the coordinates from user input are type: int, and in
    range BOARD_SIZE otherwise print message with a problem description
    and call again the function until the input contains only correct
    values
    """
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
    """
    Check if the chosen field is not already filled.
    """
    try:
        if not data[r][c] == '_':
            print(f'The field with coordinates ({r}, {c}) is not free!')
            return False
        return True
    except IndexError:
        print('Please, enter 2 numbers, seperated by space in range(0, 2)')
        return


def check_sequence(seq):
    """
    check if the given sequence contains only equal elements
    different from EMPTY_FIELD
    """
    if seq[0] == EMPTY_FIELD:
        return EMPTY_FIELD
    if all([seq[0] == elem for elem in seq[1:]]):
        return seq[0]

    return EMPTY_FIELD


def check_rows(data):
    """
    Check if every row contains only equal elements different
    from EMPTY_FIELD
    """
    for row in data:
        check = check_sequence(row)
        if check != EMPTY_FIELD:
            return check
    return EMPTY_FIELD


def check_columns(data):
    """
    Check if every column contains only equal elements different
    from EMPTY_FIELD
    """
    for col in range(BOARD_SIZE):
        columns = []
        for row in range(BOARD_SIZE):
            columns.append(data[row][col])
        check = check_sequence(columns)
        if check != EMPTY_FIELD:
            return check
    return EMPTY_FIELD


def check_primary_diagonal(data):
    """
    Check if the primary diagonal contains only equal elements different
    from EMPTY_FIELD
    """
    diagonal = []
    for i in range(BOARD_SIZE):
        diagonal.append(data[i][i])
    check = check_sequence(diagonal)
    if check != EMPTY_FIELD:
        return check
    return EMPTY_FIELD


def check_secondary_diagonal(data):
    """
    Check if the secondary diagonal contains only equal elements different
    from EMPTY_FIELD
    """
    diagonal = []
    for i in range(BOARD_SIZE):
        diagonal.append(data[i][BOARD_SIZE - i - 1])
    check = check_sequence(diagonal)
    if check != EMPTY_FIELD:
        return check
    return EMPTY_FIELD


def get_current_empty_fields(board):
    """
    Collect and return all empty fields coordinate from the
    given board.
    """
    empty_fields_coordinates = []

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY_FIELD:
                empty_fields_coordinates.append((row, col))
    if len(empty_fields_coordinates) > 0:
        return empty_fields_coordinates
    return False


def make_move(coordinates, player, board):
    """
    Filled the given board field with the player's sign
    """
    board[coordinates[0]][coordinates[1]] = player


def view_board_state(board):
    """
    Print the current board state
    """
    for row in board:
        print(' '.join([str(x) for x in row]))
    print('\n')


def check_for_winner(player, board):
    """
    Check if there is a win.
    """
    if check_rows(board) == player or \
            check_columns(board) == player or \
            check_primary_diagonal(board) == player or \
            check_secondary_diagonal(board) == player:
        return True
    return False


def maximizing_move(board, player, empty_fields):
    best_score = -sys.maxsize
    for field in empty_fields:
        row, col = field
        board[row][col] = player
        score = minimax(board, False)
        board[row][col] = EMPTY_FIELD
        if score > best_score:
            best_score = score
    return best_score


def minimizing_move(board, player, empty_fields):
    best_score = sys.maxsize
    for field in empty_fields:
        row, col = field
        board[row][col] = player
        score = minimax(board, True)
        board[row][col] = EMPTY_FIELD
        if score < best_score:
            best_score = score
    return best_score


def memoize(func):
    memo = {}

    def wrapper(board, player):
        board_as_str = str(board)
        if (board_as_str, player) not in memo:
            memo[(board_as_str, player)] = func(board, player)
        return memo[board_as_str, player]
    return wrapper


@memoize
def minimax(board, is_maximizing):
    """
    Search for the best score until reach one of the terminal states.

    """
    if check_for_winner(PLAYER_X, board):
        return -1

    if check_for_winner(PLAYER_AI, board):
        return +1

    if not get_current_empty_fields(board):
        return 0

    empty_fields_list = get_current_empty_fields(board)
    current_board = copy.deepcopy(board)
    if is_maximizing:
        return maximizing_move(current_board, PLAYER_AI, empty_fields_list)

    else:
        return minimizing_move(current_board, PLAYER_X, empty_fields_list)


def find_best_ai_move(board, empty_fields_coordinates):
    """
    Return the best move for AI based on MinMax algorithm
    """
    best_score = -sys.maxsize
    best_move = None
    for field in empty_fields_coordinates:
        row, col = field
        board[row][col] = PLAYER_AI
        score = minimax(board, False)
        board[row][col] = EMPTY_FIELD
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move


def main():
    """
    Initialize a board and messages with information about the
    game state after every move.
    If there is a win or all of the board fields are filled, the game ends.
    """

    game_board = generate_board()
    view_board_state(game_board)

    while True:
        print('Enter your move in order row col:')
        coordinates = is_valid_move()

        while not check_is_free_field(coordinates[0], coordinates[1], game_board):
            print('Enter your move again:')
            coordinates = is_valid_move()

        make_move(coordinates, PLAYER_X, game_board)
        view_board_state(game_board)

        if check_for_winner(PLAYER_X, game_board):
            print(f'*** The WINNER is PLAYER ***')
            break

        if get_current_empty_fields(game_board):
            ai_coordinates = find_best_ai_move(game_board, get_current_empty_fields(game_board))
            make_move(ai_coordinates, PLAYER_AI, game_board)
            view_board_state(game_board)
            if check_for_winner(PLAYER_AI, game_board):
                print(f'*** The WINNER is AI ***')
                break

        if not get_current_empty_fields(game_board):
            print(f'Game over! We don\'t have a winner!')
            break


if __name__ == '__main__':
    main()
