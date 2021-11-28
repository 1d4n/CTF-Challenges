import socket


def init_conn(conn, host, port):
    conn.connect((host, port))
    conn.recv(1024)
    print(conn.recv(8).decode())  # GO!


def get_words():
    with open('words.txt', 'r') as w:
        w_list = w.read().split('\n')
    return w_list[:-1]


def common_letters(words_list, current_word, number):
    filtered_list = []
    for word in words_list:
        counter = 0
        for char in current_word:
            if char in word:
                counter += 1
            if counter == number:
                filtered_list.append(word)
                break
    return filtered_list


if __name__ == '__main__':
    found = False
    attempts = 0
    
    while not found:
        print('---------------------------')
        print("Connecting to the server...")
        attempts += 1
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            init_conn(s, 'tricky-guess.csa-challenge.com', 2222)
            
            words = get_words()
            for i in range(1, 16):
                print(f"#{i}: ({len(words)} possible words)")
                word_to_send = words.pop()
                print("Sending the word:", word_to_send, end="")
                s.send(word_to_send.encode() + b'\n')
                
                resp = s.recv(64).decode()
                if len(resp) > 3:
                    print("\nThe flag is:", resp)
                    found = True
                    break
                
                print("\nCommon letters:", resp)
                words = common_letters(words, word_to_send, int(resp))
        
        print("Total attempts:", attempts)
