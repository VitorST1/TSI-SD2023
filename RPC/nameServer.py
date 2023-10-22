# nameServer.py

from rpc.nameServer import NameServer

HOST = '10.3.1.37'
PORT = 5000

server = NameServer(HOST, PORT)

if __name__ == '__main__':
    server.start()