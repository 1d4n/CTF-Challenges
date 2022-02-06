def triangular_generator():
    # 0, 1, 3, 6, 10, ...
    n = 0
    while True:
        yield (n * (n + 1)) // 2  # sum of arithmetic sequence with d = 1
        n += 1


def get_bytes(file, header_size):
    file.read(header_size)
    return list(file.read(-1))


def bin_to_dec(bits):
    # return int(''.join(map(str, bits)), 2)  # one line
    res = 0
    mul = 1
    for i in range(len(bits) - 1, -1, -1):
        res += bits[i]*mul
        mul *= 2
    return res


def extract_lsb(data):
    res = []
    gen = triangular_generator()
    count, bits = 0, [0]*8
    while (num := next(gen)) < len(data):
        bits[count % 8] = data[num] % 2  # extracting the LSB (least significant bit)
        count += 1
        if count % 8 == 0:  # checking if we have a byte
            res.append(bin_to_dec(bits))
    return ''.join(map(chr, res))


if __name__ == "__main__":
    # Header size of bmp file: 1078 bytes
    flag = extract_lsb(get_bytes(open("challenge_files/challenge.bmp", "rb"), 1078))
    print(flag)
