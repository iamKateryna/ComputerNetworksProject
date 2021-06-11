import socket
import threading
import parser
from method import LinearModel
import json
from database import *

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg[:8] == "GEN_LINK":
                ident = int(msg[8:])
                obj = db.session.query(History).get(ident)
                return_dict = {'matrix': obj.matrix, 'b_vector': obj.b_vector, 'c_vector': obj.c_vector,
                               'opt_val': obj.opt_val, 'x_vector': obj.x_vector}
                return_dict = json.dumps(return_dict)
                conn.send(return_dict.encode(FORMAT))
            else:
                A, b, c = parser.parse_json(msg)
                dictionary = json.loads(msg)

                model1 = LinearModel()

                model1.addA(A)
                model1.addB(b)
                model1.addC(c)
                model1.setObj("MAX")

                result_x, result_ans, result_iter = model1.optimize()

                new_row = History(matrix=dictionary['matrix'],
                                  b_vector=dictionary['vector_b'],
                                  c_vector=dictionary['vector_c'],
                                  opt_val=str(result_ans),
                                  x_vector=str(result_x))
                try:
                    db.session.add(new_row)
                    db.session.commit()
                except:
                    pass

                a = {'result_x': str(result_x), 'result_ans': str(result_ans),
                     'result_iter': str(result_iter), 'result_id': str(new_row.id)}
                a = json.dumps(a)

                conn.send(a.encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
