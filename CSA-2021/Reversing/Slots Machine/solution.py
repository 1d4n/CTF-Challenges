import random
import requests
import prng_recover

flag = "CSA{THAT_WAS_A_NICE_CHALLENGE:)}"
PRINTABLE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+-/:.;<=>?@[]^_`{}"  # len = 64
flag_len = len(flag)  # 32

CHUNK_SIZE = 6
RAND_NUM_LEN = 192
URL = "http://slot-machine-reloaded.csa-challenge.com"
random_32bits_list = []


class SlotMachine(object):
    def __init__(self):
        seed = random.SystemRandom().getrandbits(64)
        self.random = random.Random(seed)  # we can restore it and reveal the "random" numbers
        self.slots = [list(PRINTABLE) for _ in range(flag_len)]
        self.attempt_num = 0

    def prepend_flag(self):
        for i in range(flag_len):
            self.slots[i].remove(flag[i])
            self.slots[i] = [flag[i]] + self.slots[i]

    def choice(self):
        r = self.random.getrandbits(RAND_NUM_LEN)
        rand_num = format(r, '0%db' % RAND_NUM_LEN)  # same as: format(r,'#0194b')[2:]
        result, j = "", 0
        for i in range(len(flag)):
            chunk = rand_num[CHUNK_SIZE * i: CHUNK_SIZE * (i + 1)]
            idx = int(chunk, 2)
            result += self.slots[j][idx]
            j += 1
        return result

    def spin(self):
        if self.attempt_num == 200:
            self.prepend_flag()
        result = self.choice()
        self.attempt_num += 1
        return result


def reverse_result(result):
    rand = ''.join([format(PRINTABLE.index(x), '0%db' % CHUNK_SIZE) for x in result])
    chunks = get_chunks(rand, CHUNK_SIZE)
    int_list = [int(c, 2) for c in chunks]
    return int_list


def get_chunks(binary_str, amount):
    size = len(binary_str) // amount
    return [binary_str[size * i: size * (i + 1)] for i in range(amount - 1, -1, -1)]


def restore_rand(int_list):
    return ''.join([format(i, '032b') for i in int_list][::-1])


def get_next_32bit_ints(prng):
    next_list = []
    for i in range(CHUNK_SIZE):
        next_list.append(prng.getrandbits(32))  # = prng._randbelow((1<<32) - 1)
    return next_list


def get_indexes_from_rand_str(rand_num_str):
    return [int(rand_num_str[CHUNK_SIZE * i: CHUNK_SIZE * (i + 1)], 2) for i in range(flag_len)]


def get_indexes_from_result(result, printable):
    return [printable.index(c) for c in result]


def is_one_option(options_list):
    for option in options_list:
        if len(option) > 1:
            return False
    return True


def reduce_options(options, result_idx_list, original_idx_list):
    for i in range(len(result_idx_list)):
        original_idx = original_idx_list[i]
        result_idx = result_idx_list[i]
        c = PRINTABLE[result_idx]
        if c not in options[i]:
            continue
        if original_idx == 0:
            options[i] = [c]
        elif result_idx == original_idx:
            options[i] = options[i][:options[i].index(c)]
        else:
            options[i] = options[i][options[i].index(c):]


def get_flag(spin_func):
    print("Spinning 200 times in order to restore the PRNG (Pseudorandom number generator) and to prepend the flag")
    print("0%", end='\t')
    print(''.join(('|' if i % 10 == 0 else '*' for i in range(100))), end=' ')
    print("100%", end="\n\t")

    for i in range(200):
        if i % 2 == 0:
            print('-', end='')
        result = spin_func()
        random_32bits_list.extend(reverse_result(result))

    original_prng = prng_recover.get_prng(random_32bits_list)
    flag_options = [list(PRINTABLE) for _ in range(flag_len)]
    print("", "The PRNG has been restored.", "Spinning in order to reduce options for the flag...", sep="\n")
    while not is_one_option(flag_options):
        result = spin_func()
        rand_num = restore_rand(get_next_32bit_ints(original_prng))
        reduce_options(flag_options, get_indexes_from_result(result, PRINTABLE), get_indexes_from_rand_str(rand_num))

    print("\nThe flag is:", ''.join(c[0] for c in flag_options))


def remote_spin(session):
    return session.get(URL + "/spin/?coins=1").json()["result"]


def get_spin_func(is_local_spin):
    if is_local_spin:
        s = SlotMachine()
        return lambda: s.spin()
    s = requests.session()
    s.get(URL)
    return lambda: remote_spin(s)


if __name__ == "__main__":
    is_local = True  # change to False if you want to spin remotely
    get_flag(get_spin_func(is_local))
