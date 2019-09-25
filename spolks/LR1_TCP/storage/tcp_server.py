import os
import socket
import datetime
import sys
from time import perf_counter, sleep

from constants import MAX_QUERY_SIZE, SOCKET_PORT
# from spolks.LR1_TCP.constants import MAX_QUERY_SIZE, SOCKET_PORT


def speed(buf, t0, t1):
    return round(len(buf)/(t1-t0)/1024**2, 2)


class TCPServer:
    SERVER_STOPPED_MESSAGE = b'SERVER STOPPED!'
    LOG_FILE = 'server_log_{}.log'

    RECEIVE_BUFFER_SIZE = 1024
    TIMEOUT = 60

    LOG_DIR = 'logs'
    STORAGE_DIR = 'storage'

    def __init__(self, host='', port=SOCKET_PORT, max_client_count=MAX_QUERY_SIZE, sock=None, log_file=None):
        self.max_client_count = max_client_count
        self.host = host
        self.port = port
        self.server_address = (self.host, self.port)
        self.socket = sock

        self.log_file = log_file
        self._start_logging()

        self.connections = []

    def _start_logging(self):
        cur_dir = os.path.abspath(os.path.curdir)
        storage_path = os.path.join(cur_dir, self.STORAGE_DIR)
        log_path = os.path.join(cur_dir, self.LOG_DIR)

        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

        if not os.path.exists(log_path):
            os.mkdir(log_path)

        log_file = os.path.join(
            log_path,
            self.LOG_FILE.format(datetime.datetime.now().strftime('%d.%m.%Y__%H.%M.%S'))
        )

        if not self.log_file or self.log_file.closed:
            self.log_file = open(log_file, 'w')

        self.__log('server created')
        self.__log(f'server storage path {storage_path}')
        self.__log(f'server log path {log_path}')

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        self.__log(f'server ip address: port = {ip_address}:{self.port}')
        self.log_file.close()
        self.LOG_FILE = log_file

    def _open_socket(self):
        self.socket.listen(self.max_client_count)
        self.__log(f'open socket for {self.max_client_count} clients')

    def _create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 60)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 10)


        sock.bind(self.server_address)

        self.__log(f'create socket {sock}')

        return sock

    def _wait_client(self):
        conn, addr = self.socket.accept()
        #
        # conn.settimeout(self.TIMEOUT)
        self.connections.append((conn, addr))

        self.__log(f'new client connected {addr}')

        return conn, addr

    def _client_processing(self, connection, addr):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        while True:
            data = connection.recv(self.RECEIVE_BUFFER_SIZE)
            connection.settimeout(self.TIMEOUT)
            if not data:
                return

            command, *params = data.split(b' ')
            self.__log(f'client {addr} send commend {command} with params {params}')

            if command == b'ping':
                connection.send(b'pong')
            elif command == b'pong':
                connection.send(b'ping')
            elif command == b'help':
                connection.send(b'''help - to see list of commands
ping - test that the server is alive
kill - to stop server
echo - to resent message to a client
upload - to upload file to the server `upload file_name_on_your_machine.extension file_name_on_server`
download - to download file from a server `download file_name_on_server`
time - get server time
''')
            elif command == b'kill':

                connection.send(b'GoodBy!')
                return -1
            elif command == b'echo':
                connection.send(b' '.join(params))
            elif command == b'upload':
                self.upload_file(connection, params[0].decode(encoding='utf-8'))

            elif command == b'download':
                connection.settimeout(4)
                data = self.download_file(connection, params)

                connection.send(b'')
            elif command == b'time':
                connection.send(str(datetime.datetime.now().time()).encode(encoding='utf-8'))
            else:
                connection.send(b'unknown command, please try again')

            connection.close()

    def _close_connection(self, connection):
        client = list(filter(lambda x: x[0] == connection, self.connections))[0]

        self.__log(f'connection closed {client[1]}')
        self.connections.remove(client)
        try:
            client.send(b'connection closed press enter')
        except Exception as e:
            pass

    def _start_server(self):
        os.chdir(self.STORAGE_DIR)
        self.__log('server started')

        while True:
            try:
                conn, addr = self._wait_client()

                action = self._client_processing(connection=conn, addr=addr)

                if action == -1:
                    return

                self._close_connection(conn)
            except ConnectionResetError as e:
                self.__log(str(e))
                self._close_connection(conn)
            except Exception as e:
                self.__log(str(e))
                self._close_connection(conn)

    def __log(self, message):
        if self.log_file.closed:
            self.log_file = open(self.LOG_FILE, 'a')

        print(f'{datetime.datetime.now()}: {message}')
        self.log_file.write(f'{datetime.datetime.now()}: {message}\n')

    def stop(self):
        for conn, addr in self.connections:
            if not conn.close:
                conn.send(self.SERVER_STOPPED_MESSAGE)
                conn.close()
                self.__log(f'{conn} closed by server')

        self.socket.close()

        self.__log(f'socket closed')
        self.__log(f'server stopped')

        self.log_file.close()

    def run(self):
        self.socket = self.socket if self.socket else self._create_socket()
        self._open_socket()

        try:
            self._start_server()
            self.stop()
        except KeyboardInterrupt as e:
            self.__log(str(e))
            self.stop()

    @staticmethod
    def upload_file(sock, file_name):
        _speed = []
        print('Download to server')
        f = None
        try:
            link_count = 0

            f = open(file_name, 'wb')
            i = -1
            count = 0
            ss = []

            size = None
            rec_size = 0

            while True:
                try:
                    i += 1

                    t0 = perf_counter()
                    data = sock.recv(1024)

                    if not size:
                        size = data.split(b' ')[0]
                        print(size)
                        size = int(size.decode(encoding='utf-8'))
                        data = b' '.join(data.split(b' ')[1:])

                    t1 = perf_counter()

                    if not i % 20:
                        s = speed(data, t0, t1)
                        ss.append(s)
                        count += 1

                    if data:
                        f.write(data)
                        rec_size += len(data)
                        link_count = 0
                    else:

                        f.close()
                        print('\nfile end')
                        print(f'average speed {round(sum(ss) / count, 2)} Mb/s')
                        break

                except Exception as e:
                    if str(e) == 'timed out':
                        print(f'\n{str(e)}, count {str(link_count)}')
                        link_count += 1

                        if link_count > 3:
                            raise ConnectionError
                    else:
                        print(f'\nSome error inside WHILE put file:{str(e)}')
                        break

        finally:
            print('')
            if f:
                f.close()

    @staticmethod
    def download_file(connection, params):
        print('Upload to client')
        name_string = params[0]
        f = None
        try:
            link_count = 0
            f = open(name_string, 'rb')
            size = os.path.getsize(name_string)
            connection.send(f'{size} '.encode(encoding='utf-8'))

            i = -1
            while True:
                # Time out внутри этого try считается за обрыв. Ждем три раза
                try:
                    i += 1
                    data = f.read(1024)
                    if data:
                        connection.send(data)
                        link_count = 0
                    else:
                        connection.close()
                        break

                except Exception as e:
                    if str(e) == 'timed out':
                        print(f'\n{str(e)}, count {str(link_count)}')
                        link_count += 1
                        if link_count > 3:
                            raise ConnectionError
                    else:
                        print(f'\nSome error inside WHILE put file:{str(e)}')
                        break
        except ConnectionError:
            print(f'\nConnection Error. Timed out')
        except Exception as e:
            print(f'\nError while sending file: {str(e)}')
            connection.send(bytes(str(e), encoding='utf-8'))
        finally:
            print('')
            if f:
                f.close()


def start_server():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    sock = socket.socket()
    sock.bind(('192.168.43.212', 54320))
    sock.listen(MAX_QUERY_SIZE)

    print('-' * 5, 'TCP Server v1.0 started', '-' * 5)
    print(f'server ip address = {ip_address}')

    while True:
        try:
            conn, addr = sock.accept()
            print(f'new connection addr : {addr}')
            while True:
                data = conn.recv(1024)

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
                elif command == b'send':
                    if params[0] == b'file':
                        with open(params[1].decode(encoding="utf-8"), 'ab') as file:
                            file.write(params[2])
                            while True:
                                data = conn.recv(1024)

                                if not data:
                                    break
                                else:
                                    file.write(data)

                        print(f'receive file {params[1].decode(encoding="utf-8")}')
                        data = b'ok'
                elif command == b'time':
                    data = str(datetime.datetime.now().time()).encode(encoding='utf-8')
                else:
                    print(f'receive from {addr} data: {data.decode(encoding="utf-8")}')

                conn.send(data)

            print(f'close connection on : {conn}')
            conn.close()
        except Exception as e:
            print(f'SERVER ERROR {e}')
        except KeyboardInterrupt as e:
            if conn:
                conn.close()
            sock.close()
            print('SERVER STOP')
            sys.exit(-1)


if __name__ == '__main__':
    # start_server()
    server = TCPServer()
    server.run()
