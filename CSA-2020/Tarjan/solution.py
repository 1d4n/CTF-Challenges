import json


def lca(a, b):
    while a != b:
        if a > b:
            a = (a-1) // 2
        else:
            b = (b-1) // 2

    return a


if __name__ == '__main__':
    with open('tree.txt', 'r') as f:
        tree = f.read()

    with open('pairs.txt', 'r') as f:
        pairs = json.load(f)

    flag = ''.join((tree[lca(pair[0], pair[1])] for pair in pairs))
    print("The flag is:", flag)
