import copy
import random
import sys

EMPTY_FIELD = '_'
PLAYER_X = 'X'
PLAYER_AI = 'O'
BOARD_SIZE = 3


def board_to_hash(board):
    return hash(tuple(tuple(row) for row in board))


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

    if not data[r][c] == '_':
        print(f'The field with coordinates ({r}, {c}) is not free!')
        return False
    return True


def check_sequence(seq):
    """
    check if the given sequence contains only equal elements
    different from EMPTY_FIELD
    """
    if seq[0] != EMPTY_FIELD and all([seq[0] == elem for elem in seq[1:]]):
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
    return (check_rows(board) == player
            or check_columns(board) == player
            or check_primary_diagonal(board) == player
            or check_secondary_diagonal(board) == player)


def change_player(current_player: bool):
    """
    Change the current player
    """
    return not current_player


def pick_player(current_player: bool):
    """
    Return current player sign
    """
    return PLAYER_X if current_player else PLAYER_AI


def make_comparison(operator, maxsize, score):
    """
    Make comparison based on operator
    """
    return eval(f'{score}{operator}{maxsize}')


def min_max_moves(board, player, empty_fields):
    best_score = -sys.maxsize
    operator = '>'
    if player:
        best_score = sys.maxsize
        operator = '<'
    for field in empty_fields:
        row, col = field
        board[row][col] = pick_player(player)
        score = minimax(board, change_player(player))
        board[row][col] = EMPTY_FIELD
        if make_comparison(operator, best_score, score):
            best_score = score
    return best_score


def minimax(board, player, memo={}):
    """
    Search for the best score until reach one of the terminal states.
    """
    memo_score = memo.get(board_to_hash(board), None)
    if memo_score is not None:
        return memo_score

    if check_for_winner(PLAYER_X, board):
        return -1

    if check_for_winner(PLAYER_AI, board):
        return +1

    if not get_current_empty_fields(board):
        return 0

    empty_fields_list = get_current_empty_fields(board)
    current_board = copy.deepcopy(board)
    s = min_max_moves(current_board, player, empty_fields_list)
    memo[board_to_hash(current_board)] = s
    return s


def find_best_ai_move(board, empty_fields_coordinates):
    """
    Return the best move for AI based on MinMax algorithm
    """
    best_score = -sys.maxsize
    best_move = None
    for field in empty_fields_coordinates:
        row, col = field
        board[row][col] = PLAYER_AI
        score = minimax(board, True)
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
    coordinates = None
    player = True

    while True:
        if player:
            print('Enter your move in order row col:')
            coordinates = is_valid_move()

            while not check_is_free_field(coordinates[0], coordinates[1], game_board):
                print('Enter your move again:')
                coordinates = is_valid_move()
        else:
            if get_current_empty_fields(game_board):
                coordinates = find_best_ai_move(game_board, get_current_empty_fields(game_board))

        make_move(coordinates, pick_player(player), game_board)
        view_board_state(game_board)

        if check_for_winner(pick_player(player), game_board):
            player_name = 'PLAYER' if player else 'AI'
            print(f'*** The WINNER is {player_name} ***')
            break

        if not get_current_empty_fields(game_board):
            print(f'Game over! We don\'t have a winner!')
            break

        player = change_player(player)


if __name__ == '__main__':
    main()
