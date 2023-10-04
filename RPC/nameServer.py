# nameServer.py

from rpc.nameServer import NameServer

HOST = '127.0.0.1'
PORT = 5000

server = NameServer(HOST, PORT)

if __name__ == '__main__':
    server.start()