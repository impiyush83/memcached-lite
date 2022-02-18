import unittest
import socket


class TestSingleClient(unittest.TestCase):

    def test_success_set_command(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        test_server_port = 5001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, test_server_port))
        commands = []
        for i in range(0, 5):
            commands.append("set test" + str(i) + ' ' +
                            str(len(str(i))) + ' ' + str(i))
        for command in commands:
            print(command)
            sock.sendall(command.encode('utf-8'))
            data = sock.recv(1024)
            print(data.decode('utf-8'))
            assert data.decode('utf-8') == 'STORED\r\n'

    def test_failure_set_command_invalid(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        test_server_port = 5001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, test_server_port))
        commands = []
        for i in range(0, 5):
            commands.append("set test" + str(i) + ' ' +
                            '20 ' + str(i))
        for command in commands:
            print(command)
            sock.sendall(command.encode('utf-8'))
            data = sock.recv(1024)
            print(data.decode('utf-8'))
            assert data.decode('utf-8') == 'NOT_STORED\r\n'

    def test_failure_set_command_invalid_key_length(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        test_server_port = 5001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, test_server_port))
        commands = []
        for i in range(0, 5):
            commands.append("set test" + '5'*500 + ' ' +
                            '500 ' + str(i))
        for command in commands:
            print(command)
            sock.sendall(command.encode('utf-8'))
            data = sock.recv(1024)
            print(data.decode('utf-8'))
            assert data.decode('utf-8') == 'ERROR\r\n'


if __name__ == '__main__':
    unittest.main()
