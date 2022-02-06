# Timing Attack
import subprocess
from timeit import default_timer as timer


def read(process):
    msg = process.stdout.readline()
    process.stdout.readline()
    process.stdout.flush()
    return msg


def write(process, msg):
    process.stdin.write((msg + '\n').encode())
    process.stdin.flush()


def calc_time(process, msg):
    start = timer()
    write(process, msg)
    read(process)
    return timer() - start


def get_flag_len(process, flag_len_range):
    curr = []
    res = max_time = 0
    for i in range(flag_len_range):
        curr.append('?')
        curr_time = calc_time(process, ''.join(curr))
        if curr_time > max_time:
            max_time = curr_time
            res = i + 1  # current length
    return res


def get_flag(process, flag_len, delay, printable):
    prev_time = delay
    password = ['?'] * flag_len
    for i in range(flag_len - 1):
        for c in printable:
            password[i] = c
            flag = ''.join(password)
            curr_time = calc_time(process, flag)
            if curr_time > prev_time + delay:
                print(flag, curr_time)
                prev_time = curr_time
                break
    # last char
    for c in printable:
        password[flag_len - 1] = c
        flag = ''.join(password)
        write(process, flag)
        if "Incorrect" not in read(process).decode():
            return flag


def main(flag_len_range, file_name, printable):
    process = subprocess.Popen(file_name, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    print(process.stdout.readline().decode())
    flag_len = get_flag_len(process, flag_len_range)
    print("The length of the flag is:", flag_len)
    flag = get_flag(process, flag_len, 0.05, printable)

    with open("flag.txt", 'w') as f:
        f.write(flag)
    print("The flag is:", flag)
    process.terminate()


if __name__ == '__main__':
    start_time = timer()
    main(100, "Pass_it_on.exe",
         "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~")
    print("Total time:", timer() - start_time, "seconds.")
