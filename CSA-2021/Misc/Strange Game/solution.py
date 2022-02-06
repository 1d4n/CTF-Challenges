import re
from pwnlib.tubes.remote import remote
from minimax import get_best_move

HOST = "strange-game.csa-challenge.com"
PORT = 4444
TOTAL_ROUNDS = 15


def init_connection():
    print("Connecting to the server...")
    try:
        conn = remote(HOST, PORT, timeout=3)
    except:
        print("Couldn't connect to the server")
    else:
        recv_msg(conn, b'Press any key...', True)
        return conn


def client_move(conn, client_moves, server_moves):
    choice = get_best_move(server_moves, client_moves)
    if not choice:
        return None
    msg = send_and_recv_msg(conn, choice)
    if "tied" in msg:
        return None
    return choice


def server_move(msg):
    choice = re.search("play [1-9]", msg)
    if not choice:
        return None
    return int(choice.group().replace('play ', ''))


def recv_msg(conn, until=b'', println=False):
    msg = (conn.recvuntil(until) if until else conn.recv()).decode()
    print(msg, end=('\n' if println else ''))
    return msg


def send_and_recv_msg(conn, msg):
    conn.sendline(str(msg).encode())
    print(msg)
    return recv_msg(conn)


def run(conn):
    conn.sendline(b'')  # press any key
    server_moves = set()
    client_moves = set()

    msg = recv_msg(conn, b'Choose your move: ')
    if "I'll go first" in msg:  # checking if the server is first
        server_choice = server_move(msg)
        if not server_choice:
            conn.close()
            raise Exception("Error - couldn't get server's choice from the first message")
        server_moves.add(server_choice)

    while True:
        client_choice = client_move(conn, client_moves, server_moves)
        if not client_choice:
            break
        client_moves.add(client_choice)

        server_choice = server_move(recv_msg(conn))
        if not server_choice:
            break
        server_moves.add(server_choice)


def main():
    conn = init_connection()
    if not conn:
        return
    for _ in range(TOTAL_ROUNDS):
        run(conn)
    conn.close()


if __name__ == '__main__':
    main()
