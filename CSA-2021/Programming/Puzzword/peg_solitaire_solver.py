# Source: https://github.com/VasilisG/Peg-Solitaire-Solver
import time

UP, DOWN, LEFT, RIGHT = '^', 'v', '<', '>'
EMPTY, PEG = '.', 'O'


def get_neighbor_coords(curr, direction):
    x, y = curr[0], curr[1]
    if direction == UP:
        return x, y - 1
    if direction == DOWN:
        return x, y + 1
    if direction == LEFT:
        return x - 1, y
    return x + 1, y


class Node:
    def __init__(self, mat, parent, move, pegs_count=0):
        self.mat = mat
        self.parent = parent
        self.move = move
        self.height = len(mat)
        self.width = len(mat[0])
        self.pegs_count = self.parent.pegs_count - 1 if self.parent else pegs_count

    def get_direction(self):
        src, dest = self.move[0], self.move[1]
        if dest[0] == src[0]:
            direction = DOWN if dest[1] > src[1] else UP
        else:
            direction = RIGHT if dest[0] > src[0] else LEFT
        return [src[0], src[1], direction]

    def is_finished(self, dest, dest_pegs):
        return self.pegs_count == dest_pegs and [''.join(x) for x in self.mat] == dest

    def is_valid(self, coords, symbol=PEG):
        x, y = coords[0], coords[1]
        return 0 <= x < self.width and 0 <= y < self.height and self.mat[y][x] == symbol

    def get_all_pegs(self):
        return [(x, y) for x in range(self.width) for y in range(self.height) if self.mat[y][x] == PEG]

    def get_node_after_move(self, src, neigh, dest):
        mat = [[self.mat[i][j] for j in range(self.width)] for i in range(self.height)]
        mat[src[1]][src[0]], mat[dest[1]][dest[0]] = mat[dest[1]][dest[0]], mat[src[1]][src[0]]
        mat[neigh[1]][neigh[0]] = EMPTY
        return Node(mat, self, [src, dest])

    def append_node(self, lst, src, direction):
        neigh = get_neighbor_coords(src, direction)
        dest = get_neighbor_coords(neigh, direction)
        if self.is_valid(neigh) and self.is_valid(dest, EMPTY):
            lst.append(self.get_node_after_move(src, neigh, dest))

    def get_available_nodes(self, curr):
        res = []
        for direction in UP, DOWN, LEFT, RIGHT:
            self.append_node(res, curr, direction)
        return res

    def gen_children(self):
        return [node for coords in self.get_all_pegs() for node in self.get_available_nodes(coords)]


class Solver:
    def __init__(self, src, dest, time_limit=60):
        self.start = Node(src, None, None, ''.join(src).count(PEG))
        self.is_solved = False
        self.moves = []
        self.dest = dest
        self.dest_pegs = ''.join(dest).count(PEG)
        self.time_limit = time_limit
        self.start_time = time.time()

    def get_path(self, end):
        path = []
        curr = end
        while curr.parent:
            path.append(curr)
            curr = curr.parent
        for node in path[::-1]:
            self.moves.append(node.get_direction())

    def dfs(self, node):
        if node.is_finished(self.dest, self.dest_pegs):
            self.get_path(node)
            self.is_solved = True
        elif time.time() - self.start_time < self.time_limit and not self.is_solved and node.pegs_count > self.dest_pegs:
            for child in node.gen_children():
                self.dfs(child)

    def solve(self):
        self.dfs(self.start)
        return self.moves


if __name__ == '__main__':
    s = Solver(['  OOO  ', '  OOO  ', 'OOOOOOO', 'OOO.OOO', 'OOOOOOO', '  OOO  ', '  OOO  '],
               ['  ...  ', '  ...  ', '.......', '...O...', '.......', '  ...  ', '  ...  '])
    print(s.solve())
