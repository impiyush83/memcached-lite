import unittest
import socket


class TestMultipleClient(unittest.TestCase):

    def test_success_update_set_command(self):
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        test_server_port = 5001
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock1.connect((host, test_server_port))
        sock2.connect((host, test_server_port))
        for i in range(0, 2):
            command1 = "set multiple" + str(i) + ' ' + str(len(str(i))) + ' ' +\
                      str(i)
            command2 = "set multiple" + str(i) + ' ' + str(len(str(i))) + ' ' +\
                       str(i+1)
            sock1.sendall(command1.encode('utf-8'))
            data1 = sock1.recv(1024)
            sock2.sendall(command2.encode('utf-8'))
            data2 = sock2.recv(1024)
            print(data1.decode('utf-8'))
            assert data1.decode('utf-8') == 'STORED\r\n'
            print(data2.decode('utf-8'))
            assert data2.decode('utf-8') == 'STORED\r\n'
            sock1.sendall(f'get multiple{i}'.encode('utf-8'))
            data1 = sock1.recv(1024)
            assert data1.decode('utf-8') \
                == f'VALUE multiple{i} 1\r\n {i+1} END\r\n\r\n'


if __name__ == '__main__':
    unittest.main()
