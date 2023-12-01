# nameServer.py

from rpc.nameServer import NameServer

HOST = 'localhost'
PORT = 5000

server = NameServer(HOST, PORT)

if __name__ == '__main__':
    server.start()
