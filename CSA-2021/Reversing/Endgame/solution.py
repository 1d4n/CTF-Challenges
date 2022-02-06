def calc(instruction, a, b):
    if instruction == "add":
        return a + b
    if instruction == "sub":
        return a - b
    if instruction == "mul":
        return a*b
    return a // b  # b != 0


def reverse_asm(hex_list):
    instructions_dict = {"ab": "add", "ba": "sub", "cd": "mul", "dc": "div"}
    registers_dict = {chr(i): 0 for i in range(ord('a'), ord('f') + 1)}
    is_instruction = is_register = False
    instruction = register = ""
    log = []

    for b in hex_list:
        if is_instruction:
            registers_dict[b[0]] = calc(instruction, registers_dict[b[0]], registers_dict[b[1]])
            log.append((instruction, b[0], b[1]))
            is_instruction = False
        elif is_register:
            registers_dict[register] = int(b, 16)  # hex to dec
            log.append(('mov', register, registers_dict[register]))
            is_register = False
        elif b[0] == '1' and b[1] in registers_dict.keys():
            register = b[1]
            is_register = True
        elif b in instructions_dict.keys():
            instruction = instructions_dict[b]
            is_instruction = True

    for i in log:
        print(f"{i[0]}\t\t{i[1]}, {i[2]}")

    return bytes.fromhex(f"{registers_dict['a']: x}").decode()


if __name__ == '__main__':
    with open("flag", "rb") as f:
        data = f.read().hex(' ').split()
    print("The flag is:", reverse_asm(data))
