import random


# Reverses the Mersenne Twister based on 624 observed outputs.
# Source: https://github.com/eboda/mersenne-twister-recover


def un_shift_right(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res


def un_shift_left(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res


def un_temper(v):
    """ Reverses the tempering which is applied to outputs of MT19937 """

    v = un_shift_right(v, 18)
    v = un_shift_left(v, 15, 0xefc60000)
    v = un_shift_left(v, 7, 0x9d2c5680)
    v = un_shift_right(v, 11)
    return v


def get_prng(int_list):
    result_state = None
    assert len(int_list) >= 624  # need at least 624 values

    vals = []
    for i in range(624):
        vals.append(un_temper(int_list[i]))

    if len(int_list) > 624:
        # We have additional outputs and can correctly
        # recover the internal index by bruteforce
        target = int_list[624]
        for i in range(1, 626):
            state = (3, tuple(vals + [i]), None)
            r = random.Random()
            r.setstate(state)

            if target == r.getrandbits(32):
                result_state = state
                break
    else:
        # With only 624 outputs we assume they were the first observed 624
        # outputs after a twist -->  we set the internal index to 624.
        result_state = (3, tuple(vals + [624]), None)

    rand = random.Random()
    rand.setstate(result_state)
    for i in range(624, len(int_list)):
        assert rand.getrandbits(32) == int_list[i]

    return rand
