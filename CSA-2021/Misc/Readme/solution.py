from itertools import product, islice
from challenge_files.solution_checker import check_key
from multiprocessing import Process, Event, cpu_count
from time import time


N_PROC = 2 * (cpu_count() - 1)
FLAG_PATTERN = "hey_that_is_the_great_puzzle"


def get_chars_dict(normal_words, encoded_words):
    res = dict()
    for c in (set(FLAG_PATTERN) - {'_'}):
        res[c] = set()
        for i in range(len(normal_words)):
            for j in range(len(normal_words[i])):
                if normal_words[i][j] == c and j < len(encoded_words[i]):
                    res[c].add(encoded_words[i][j])
        res[c] = list(res[c])
    res['z'] = ['z', 'Z']
    res['_'] = ['_']
    return res


def dict_to_opts_list(chars_dict: dict):
    return [['{']] + [chars_dict[c] for c in FLAG_PATTERN] + [['}']]


def calc_total_options(opts_list):
    res = 1
    for i in opts_list:
        res *= len(i)
    return res


def brute_force(keys_iterator, checker_data, found):
    start_time = time()
    for key in keys_iterator:
        if found.is_set():
            break
        if check_key(''.join(key), checker_data):
            flag = "CSA" + ''.join(key)
            print("the flag is:", flag, "total time:", time() - start_time, "seconds.")
            with open("flag.txt", 'w') as f:
                f.write(flag)
            found.set()
            break


def main():
    with open("text.txt", "r") as f:
        text = f.read().split()
    with open("leet.txt", "rb") as f:
        leet = f.read().decode().split()
    with open("challenge_files/key_checker_data", "rb") as f:
        data = f.read()

    opts = dict_to_opts_list(get_chars_dict(text, leet))
    total_options = calc_total_options(opts)
    chunk_size = total_options // N_PROC
    all_keys_iterator = product(*opts)
    found = Event()
    for i in range(N_PROC):
        start_idx = i * chunk_size
        end_idx = None if i + 1 == N_PROC else (i + 1) * chunk_size - 1
        proc = Process(target=brute_force, args=(islice(all_keys_iterator, start_idx, end_idx), data, found))
        proc.start()
    print("Cracking the key...")


if __name__ == "__main__":
    main()
