import socket
import csv
from _thread import *
from pathlib import Path


INVALID_COMMAND = 'INVALID-COMMAND\r\n'
INVALID_KEY = 'INVALID-KEY\r\n'
NOT_FOUND = 'NOT-FOUND\r\n'
END = 'END\r\n'
NOT_STORED = 'NOT-STORED\r\n'
STORED = 'STORED\r\n'

SERVER_PORT = 7001


class Server:
    MAX_CONNECTIONS = 1024
    MEMCACHE_FILENAME = 'memcache.csv'

    def __init__(self, host, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        print(f'Server: Socket binded to port {port}')
        self._socket.listen(5)
        print(f'Server: Socket listening to port {port}')
        self._connections = 0
        self._memcache_kv = dict()

    def run(self):
        while True:
            print('Waiting for client to connect......')
            client, clientaddr = self._socket.accept()

            print(f'Server: '
                  f'Accepted a connection request from {client} {clientaddr}')
            start_new_thread(self.threaded, (client,))

    def stop(self):
        print('Server: Closing socket')
        self._socket.close()

    def bootloader(self):
        csv_file = open(Server.MEMCACHE_FILENAME, 'r')
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            self._memcache_kv[line[0]] = line[1]
        csv_file.close()
        print("Server: Bootloading process done")
        print(f'Server: Memcache store currently is {self._memcache_kv.keys()}')

    def threaded(self, client):
        self._connections += 1
        if self._connections > Server.MAX_CONNECTIONS:
            if self._connections > 0:
                self._connections -= 1
                print(f'Server: Closing a thread for client {client} as'
                      f' max connections exceed')
                print(
                    f'Server: Concurrent connections '
                    f'running:{self._connections}')
                client.close()
        else:
            print(f'Server: Inside a thread for client {client}')
            while True:
                data = client.recv(1024)
                command = data.decode()
                msg = (command.lower()).split()
                if len(msg) == 0:
                    break
                reply = self.command_executor(msg)
                if reply == 'END\r\n':
                    break
                print(f'Server: Data recieved from client {data}')
                client.send(reply.encode())
            if self._connections > 0:
                self._connections -= 1
            print(f'Server: Closing a thread for client {client}')
            print(f'Server: Concurrent connections running:{self._connections}')
            client.close()

    def command_executor(self, msg):
        def handle_set(self, command):
            if len(msg) < 6:
                return INVALID_COMMAND

            key, length, value = command[1], command[2], command[4]

            if len(value) != int(length):
                return NOT_STORED

            self._memcache_kv[key] = value
            with open(Server.MEMCACHE_FILENAME, 'a') as f:
                writer = csv.writer(f)
                for key, value in self._memcache_kv.items():
                    writer.writerow([key, value])
            return STORED

        def handle_get(self, command):
            if len(command) != 3:
                return INVALID_COMMAND

            key = command[1]

            if self._memcache_kv.get(key):
                    return 'VALUE' + ' ' + key + ' ' + \
                           self._memcache_kv.get(key) + ' ' + END
            return NOT_FOUND

        def handle_end(self, command):
            return END

        context_switcher = {
            'set': handle_set,
            'get': handle_get,
            'end': handle_end
        }
        return context_switcher[msg[0]](self, msg)


if __name__ == '__main__':
    try:
        server = Server('127.0.0.1', SERVER_PORT)
        server.bootloader()
        server.run()
        server.stop()
    except Exception as e:
        print(e)
