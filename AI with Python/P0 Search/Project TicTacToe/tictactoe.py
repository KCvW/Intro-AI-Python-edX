"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    list_board = [field for row in board for field in row]
    return X if list_board.count(EMPTY) % 2 != 0 else 0


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in enumerate(board):
        if EMPTY in row [1]: # we skip if no EMPTY values are left
            for field in enumerate(row[1]):
                if field[1] == EMPTY:
                    actions.add((row[0], field[0]))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # activate current player
    current_player = player(board)
    deepcopy_board = copy.deepcopy(board)
    # change current field to play further
    row = action[0]
    col = action[1]
    if deepcopy_board[row][col] == EMPTY:
        deepcopy_board[row][col] = current_player
        return deepcopy_board
    else:
        raise Exception("Move is invalid")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # verify rows if there is a winner
    for row in board:
        if len(set(row)) == 1 and EMPTY not in row:
            return X if X in row else 0
    # check for columns
    for n in range(0,3):
        col = [row[n] for row in board]
        if len(set(col)) == 1 and EMPTY not in col:
            return X if X in col else 0
    # check for winner in diagonal
    d1 = [board[el][el] for el in range(0,3)]
    if len(set(d1)) == 1 and EMPTY not in d1:
        return X if X in d1 else 0
    # check for winner in second diagonal
    board = list(reversed(board))
    d2 = [board[el][el] for el in range (0,3)]
    if len(set(d2)) == 1 and EMPTY not in d2:
        return X if X in d2 else 0


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    else:
        board = [field for row in board for field in row]
        if EMPTY in board:
            return False
        else:
            return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == 0:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        current_player = player(board)
        if current_player == X:
            v = -math.inf
            for action in actions(board):
                best_v = min_value(result(board,action))
                if best_v > v:
                    v = best_v
                    optimal_action = action
        else:
            v = math.inf
            for action in actions(board):
                best_v = max_value(result(board,action))
                if best_v < v:
                    v = best_v
                    optimal_action = action
        return optimal_action
    
    
def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    return v