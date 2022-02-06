import re


def encode_book(book, morse_dict, space_char, new_line_char):
    res = ""
    for c in book:
        res += morse_dict[c.lower()] + space_char if c.lower() in morse_dict.keys() else new_line_char
    return res


def get_regex(pattern, space_char, new_line_char):
    res = new_line_char
    for c in pattern:
        res += ("[.-]" if c == 'x' else f"[{c}]") + f"[{space_char}{new_line_char}]{{0,2}}"
    return res


def find_match(encoded_text, regex):
    return re.findall(regex, encoded_text)


def decode(morse_code, decode_dict, space_char, new_line_char):
    encoded_words = morse_code.split(new_line_char)
    res = []
    for word in encoded_words:
        decoded = ""
        for c in word.split(space_char):
            if c in decode_dict.keys():
                decoded += decode_dict[c]
        if decoded:
            res.append(decoded)
    return '_'.join(res)


def print_flag(book, flag_pattern, morse_dict, space_char, new_line_char):
    decode_dict = {morse_dict[k]: k for k in morse_dict.keys()}
    encoded_book = encode_book(book, morse_dict, space_char, new_line_char)
    regex = get_regex(flag_pattern, space_char, new_line_char)
    for match in find_match(encoded_book, regex):
        flag = decode(match, decode_dict, space_char, new_line_char)
        print(f"CSA{{{flag}}}")


if __name__ == "__main__":
    sequence_pattern = "x.xx...x.xxx..-xx-.xxxx.-.-xxx.-.x..x.xxxx..x.xxx.-.-.xx-.-xxx..-.xx.x.x.--x.xxx"
    morse = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
                  'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
                  'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
                  'y': '-.--', 'z': '--..'}
    with open("challenge_files/book.txt", "rb") as f:
        text = f.read().decode()

    print_flag(text, sequence_pattern, morse, ':', ";")
