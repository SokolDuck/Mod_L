import socket

from spolks.LR1_TCP.constants import MAX_QUERY_SIZE, CONNECTION_DATA


def start_server():
    sock = socket.socket()
    sock.bind(CONNECTION_DATA)
    sock.listen(MAX_QUERY_SIZE)

    print('-' * 5, 'TCP Server v1.0 started', '-' * 5)

    while True:
        conn, addr = sock.accept()
        print(f'new connection : {conn}, addr : {addr}')
        while True:
            data = conn.recv(1024)
            print(f'receive from {addr} data: {data.decode(encoding="utf-8")}')

            if not data:
                break

            command, *params = data.split(b' ')

            if command == b'ping':
                data = b'pong'
            elif command == b'kill':
                conn.send(b'GoodBy!')
                conn.close()
                sock.close()
                return
            elif command == b'echo':
                data = b' '.join(params)

            conn.send(data)

        print(f'close connection on : {conn}')
        conn.close()


if __name__ == '__main__':
    start_server()
