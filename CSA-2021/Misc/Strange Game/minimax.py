# Source: https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py
from itertools import combinations

CLIENT = 1
SERVER = -1
DRAW = 0

TARGET_SUM = 15
TARGET_NUMS_AMOUNT = 3
STARTING_CHOICE = 5
ALL_MOVES = set(range(1, 10))


def evaluate(server_moves, client_moves):
    if is_winner(client_moves):
        return CLIENT
    if is_winner(server_moves):
        return SERVER
    return DRAW


def is_winner(moves):
    if len(moves) < TARGET_NUMS_AMOUNT:
        return False
    for i in combinations(moves, TARGET_NUMS_AMOUNT):
        if sum(i) == TARGET_SUM:
            return True
    return False


def minimax(server_moves: set, client_moves: set, depth, is_client):
    if (winner := evaluate(server_moves, client_moves)) or depth <= 0:
        return winner

    best = SERVER-1 if is_client else CLIENT+1
    curr_moves = client_moves if is_client else server_moves
    for move in ALL_MOVES - server_moves - client_moves:  # all available moves
        curr_moves.add(move)
        score = minimax(server_moves, client_moves, depth - 1, not is_client)
        curr_moves.remove(move)
        best = max(best, score) if is_client else min(best, score)

    return best


def get_best_move(server_moves, client_moves):
    best_move = 0
    best_score = SERVER-1

    if len(server_moves) == len(client_moves) == 0:
        return STARTING_CHOICE

    available_moves = ALL_MOVES - server_moves - client_moves
    for move in available_moves:
        client_moves.add(move)
        move_score = minimax(server_moves, client_moves, len(available_moves)-1, False)
        if move_score > best_score:
            best_move = move
            best_score = move_score
        client_moves.remove(move)
    return best_move
