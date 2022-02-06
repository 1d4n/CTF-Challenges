from peg_solitaire_solver import Solver
import json as JSON
import requests
import time


def get_response(url, method, data=None):
    return (requests.get(url) if method == "get" else requests.post(url, json=data)).json()


def solve_all(request_keys, amount_of_levels):
    get = JSON.loads(get_response(request_keys["url"] + request_keys["get"], "get")[request_keys["msg"]])
    print("Round 1", get, sep="\n")
    id = get[request_keys["id"]]
    src = get[request_keys["src"]]
    dest = get[request_keys["dest"]]

    msg_list = []
    for i in range(2, amount_of_levels + 1):
        print("-------------")
        print("Round", i)
        solver = Solver(src, dest)
        sol = solver.solve()
        if not sol:
            return None

        data = {request_keys["id"]: id, request_keys["sol"]: sol}
        post = get_response(request_keys["url"] + request_keys["post"], "post", data)[request_keys["msg"]]
        print(post)
        if request_keys["err"] in post:
            return None

        if i == amount_of_levels:
            msg_list.append(post)
        else:
            try:
                resp = JSON.loads(post)
            except JSON.decoder.JSONDecodeError:
                return None
            msg_list.append(resp[request_keys["msg"]])
            id = resp[request_keys["id"]]
            src = resp[request_keys["src"]]
            dest = resp[request_keys["dest"]]
            time.sleep(1)

    return msg_list


def get_flag(request_keys, amount_of_levels):
    while True:
        start_time = time.time()
        all_messages = solve_all(request_keys, amount_of_levels)
        if not all_messages:
            print("Failed! retrying...", "--------", sep="\n")
            continue
        flag = ''.join([msg[0] for msg in all_messages[:-1]]) + all_messages[-1][-1]
        print("\nFlag:", flag)
        print("time:", time.time() - start_time)
        break


if __name__ == "__main__":
    req_keys = {"url": "https://puzzword.csa-challenge.com/", "get": "puzzle", "post": "solve", "sol": "solution",
                "id": "puzzle_id", "src": "source_board", "dest": "destination_board", "msg": "message",
                "err": "This puzzle id does not exist in our systems"}
    get_flag(req_keys, 20)
