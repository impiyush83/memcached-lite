import socket
import uuid

SERVER_PORT = 7001
HOST = '127.0.0.1'


class Client:
    MAX_BYTES = 1024
    END = "END"
    SET = "SET"
    GET = "GET"

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((HOST, SERVER_PORT))
        self._identifier = uuid.uuid4()

    def run(self):
        print(f'Client {self._identifier}: Connected to server')
        while True:
            print(f'Client {self._identifier}: Enter your input: ')
            client_input = input()
            if client_input.strip().upper() == Client.END:
                print(f'Client  {self._identifier}: Connection Closed')
                break

            action = client_input.strip().lower().split()

            if action[0].upper() == Client.SET and len(action) == 4:
                value = input().split()
                data = ' '.join(action + value)
                self._socket.sendall(data.encode())
            elif action[0].upper() == Client.GET and len(action) == 3:
                data = ' '.join(action)
                self._socket.sendall(data.encode())
            elif action[0].upper() == Client.END:
                print(f'Client  {self._identifier}: Connection Closed')
                break
            else:
                print(f'Client  {self._identifier}: Invalid commands entered '
                      f'! Try again !')
                print(f'Client {self._identifier}: \n '
                      f'1. end \n'
                      f'2. set <key> <length-of-value> \\r\\n \n'
                      f'  <value> \\r\\n  \n '
                      f'3. get <key> \\r\\n')
            print(f'Client  {self._identifier}: Waiting for server to send')
            data = self._socket.recv(Client.MAX_BYTES)
            print(f'Client {self._identifier}: Data from server {data.decode()}')

        print(f' Client  {self._identifier} : Socket closing')
        self._socket.close()

    def stop(self):
        print(f' Client  {self._identifier} : Socket closing')
        self._socket.close()


if __name__ == '__main__':
    try:
        client = Client()
        client.run()
        client.stop()
    except Exception as e:
        print(e)
