# Phillips Cipher https://www.dcode.fr/phillips-cipher
import re
from itertools import permutations
from string import ascii_uppercase
from build_grids import *

EXCLUDED_CHAR = 'J'


def grids_to_dicts(grids):
    return [{grid[i][j]: grid[(i - 1) % GRID_SIZE][(j - 1) % GRID_SIZE] for j in range(GRID_SIZE)
             for i in range(GRID_SIZE)} for grid in grids]


def decrypt(decryption_dicts, encrypted_text):
    decrypted = ['?'] * len(encrypted_text)
    curr = -1
    for i in range(len(encrypted_text)):
        if i % PERIOD == 0:
            curr = (curr + 1) % TOTAL_GRIDS
        decrypted[i] = decryption_dicts[curr][encrypted_text[i]]
    return ''.join(decrypted)


def get_flag(grids, encrypted_text):
    missing_chars = list(set(ascii_uppercase) - {grids[0][i][j] for j in range(GRID_SIZE)
                                                 for i in range(GRID_SIZE)} - {EMPTY, EXCLUDED_CHAR})
    missing_idx_list = [(i, j) for j in range(GRID_SIZE) for i in range(GRID_SIZE) if grids[0][i][j] == EMPTY]
    regex = re.compile("CSAOPENCURLYBRACKETS.+CLOSECURLYBRACKETS")  # CSA{.+}
    flag_dict = {"OPENCURLYBRACKETS": '{', "CLOSECURLYBRACKETS": '}', "UNDERSCORE": '_'}

    for p in permutations(missing_idx_list):
        for c, (i, j) in zip(missing_chars, p):
            grids[0][i][j] = c
        decrypted = decrypt(grids_to_dicts(grids), encrypted_text)
        r = regex.search(decrypted)
        if not r:
            continue
        flag = r.group()
        for key in flag_dict:
            flag = flag.replace(key, flag_dict[key])
        return flag


if __name__ == '__main__':
    encrypted = "HSVNNPBLMSXATWWPEBXTCRRCBMULAALCDLOMGRKIPALACVXMUECSWIKGVLQZDALRCAACQTBZMYAEVSMESIXDVCUWMSBLVSRBXGPQFATUMMSAQVYMVKXQERVBFLTSRATSKEERQBBXTE"
    all_grids = create_grids()
    if f := get_flag(all_grids, encrypted):
        print("The flag is:", f)
