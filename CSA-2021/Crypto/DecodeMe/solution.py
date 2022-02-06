from base64 import b32decode
import string


def xor(encrypted, key):
    res = []
    key = bytes.fromhex(key)
    key_len = len(key)
    for i in range(len(encrypted)):
        x = key[i % key_len] ^ encrypted[i]
        if x:
            res.append(chr(x))
    return res


def rot13_char(c):
    if 'z' >= c >= 'a':
        return string.ascii_lowercase[(ord(c) - ord('a') + 13) % 26]
    if 'Z' >= c >= 'A':
        return string.ascii_uppercase[(ord(c) - ord('A') + 13) % 26]
    return c


def rot13(text):
    res = []
    for c in text:
        res.append(rot13_char(c))
    return ''.join(res)


def get_flag(text, key):
    # return rot13(xor(b32decode(text), key))[::-1]  # one line

    # decode from base32  (B.XXXII)
    decoded = b32decode(text)

    # xor ((+))
    decrypted = xor(decoded, key)

    # rot13
    flag = rot13(decrypted)

    # the flag is reversed, so we need to reverse it
    return flag[::-1]


if __name__ == "__main__":
    encrypted_text = "WFKZLTABVKWVLXGMASVPYVP2ZRTKVHKV6XGBJKVEKX44YCVKXBK4XTBDVKSVL2WMACVLOVPEZQJ2VHCV"
    xor_key = "CC55AA"
    print(get_flag(encrypted_text, xor_key))
