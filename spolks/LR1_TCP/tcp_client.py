import socket

from spolks.LR1_TCP.constants import CONNECTION_DATA


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(CONNECTION_DATA)
    print('TCP Client v1.0 - SPOLKS LR !')
    print('-' * 32)
    while True:
        message = input('write message with enter in the end : \n')

        if message == 'q':
            sock.close()
            break

        sock.send(bytes(message, encoding='utf-8'))

        data = sock.recv(1024)

        print(f'recive : {data.decode(encoding="utf-8")}')
