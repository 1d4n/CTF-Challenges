import requests
import string
from base64 import b64encode
from boards_generator import create_all_boards


def is_valid(url, level, board):
    response = requests.get(url, params={"level": level, "board": board})
    return response.text == '1'


def get_shortest(url, level, boards):
    while True:
        for i in range(len(boards)):
            if is_valid(url, level, boards[i]):
                return i + 1


def get_all_shortest(url, boards, levels):
    res = []
    for level in range(levels):
        shortest = get_shortest(url, level, boards)
        res.append(shortest)
        print("---------")
        print("LEVEL", level+1, "\tshortest:", shortest)
    return res


def get_chars(shortest_list):
    res = []
    lower_chars = "_" + string.ascii_lowercase
    extended_chars = lower_chars + string.ascii_uppercase + "{}"
    for i in range(len(shortest_list)):
        options = []
        for char in (lower_chars if len(shortest_list)-1 > i > 3 else extended_chars):
            if shortest_list[i] == (ord(char) % 9) + 1:
                options.append(char)
        res.append(options)
    return res


def reduce_options(options):
    inside = options[4:-1]  # CSA{...}
    for i in range(len(inside)):
        if '_' in inside[i]:
            inside[i] = ['_']
    return [['C'], ['S'], ['A'], ['{']] + inside + [['}']]


def main(url, levels):
    boards = create_all_boards()
    encoded_boards = [b64encode((str(board)).encode()).decode() for board in boards]
    shortest_list = get_all_shortest(url, encoded_boards, levels)
    options = get_chars(shortest_list)
    print("---", "options:", reduce_options(options), sep='\n')


if __name__ == "__main__":
    main("http://memento.csa-challenge.com:7777/verifygame", 24)
