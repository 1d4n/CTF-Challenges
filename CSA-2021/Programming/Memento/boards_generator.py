import json


def distance(src, dest):
    return sum(abs(src[i] - dest[i]) for i in range(2))


def put_numbers(mat, num, shortest, use_set=True, target=20):
    if num > target:
        return True
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                for match in find_pairs(mat, (i, j), shortest, use_set):
                    mat[i][j] = mat[match[0]][match[1]] = num
                    if put_numbers(mat, num + 1, shortest, use_set, target):
                        return True
                    mat[i][j] = mat[match[0]][match[1]] = 0
    return False


def find_pairs(mat, src, shortest, use_set):
    res = set() if use_set else []
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 0 and distance(src, (i, j)) == shortest:
                res.add((i, j)) if use_set else res.append((i, j))
    return res


def create_board(shortest, height, width, use_set=True, target=20):
    board = [[0 for _ in range(width)] for __ in range(height)]
    put_numbers(board, 1, shortest, use_set, target)
    return board


def create_all_boards(distances_range=9, height=5, width=8):
    boards = []
    target = 20
    for i in range(1, distances_range + 1):
        use_set = i != 2
        # for i >= 6, it takes time to fill the whole board, so we can fill part of it
        if i == 6:
            target = 18
        elif i > 6:
            target -= 4 if i == 9 else 3
        boards.append(create_board(i, height, width, use_set, target))
    return boards


if __name__ == '__main__':
    print(create_all_boards())
