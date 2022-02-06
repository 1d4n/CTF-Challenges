PERIOD = 5
GRID_SIZE = 5
EMPTY = '?'
TOTAL_GRIDS = 8

dec = "FROMM ISTER PHILL IPSTO ALLAG ENTSS".split()
enc = "HSVNN PBLMS XATWW PEBXT CRRCB MULAA".split()
cipher_dicts_list = [{dec[i][j]: enc[i][j] for j in range(PERIOD)} for i in range(len(enc))]
keys_list = [list(d) for d in cipher_dicts_list]


def create_grids():
    grids = [[['?' for _ in range(GRID_SIZE)] for __ in range(GRID_SIZE)]]
    swap_idx = 0
    idx_list = list(range(GRID_SIZE))
    for i in range(1, TOTAL_GRIDS):
        if swap_idx + 1 >= GRID_SIZE:
            swap_idx = 0
        idx_list[swap_idx], idx_list[swap_idx + 1] = idx_list[swap_idx + 1], idx_list[swap_idx]
        grids.append([grids[0][j] for j in idx_list])
        swap_idx += 1
    put_chars(grids, 0, 0)
    return grids


def is_valid(grids, grid_idx, excluded_chars, excluded_idx_list):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if (i, j) in excluded_idx_list:
                continue
            if grids[grid_idx][i][j] in excluded_chars:
                return False
    return True


def is_all_grids_valid(grids):
    for i in range(len(enc)):
        for j in range(GRID_SIZE):
            for k in range(GRID_SIZE):
                key_cell = grids[i][j][k]
                val_cell = grids[i][(j + 1) % GRID_SIZE][(k + 1) % GRID_SIZE]
                for key, val in cipher_dicts_list[i].items():
                    if key_cell == key and val_cell not in [EMPTY, val]:
                        return False
    return True


def put_chars(grids, i, key_idx):
    if key_idx >= len(keys_list[i]):
        i += 1
        key_idx = 0
    if i >= len(enc):
        return True
    key = keys_list[i][key_idx]
    val = cipher_dicts_list[i][key]
    for j in range(GRID_SIZE):
        for k in range(GRID_SIZE):
            next_row = (j + 1) % GRID_SIZE
            next_col = (k + 1) % GRID_SIZE
            if not is_valid(grids, i, [key, val], [(j, k), (next_row, next_col)]) or grids[i][j][k] not in [EMPTY, key] \
                    or grids[i][next_row][next_col] not in [EMPTY, val]:
                continue
            if grids[i][j][k] == key and grids[i][next_row][next_col] == val:
                return put_chars(grids, i, key_idx + 1)

            prev = grids[i][j][k]
            grids[i][j][k] = key
            grids[i][next_row][next_col] = val
            if is_all_grids_valid(grids) and put_chars(grids, i, key_idx + 1):
                return True
            grids[i][j][k] = prev
            grids[i][next_row][next_col] = EMPTY
            if prev == key:
                return False

    return False


if __name__ == '__main__':
    for _grid in create_grids():
        print(*_grid, '---', sep='\n')
