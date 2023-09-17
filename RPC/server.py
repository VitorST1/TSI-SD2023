# server.py

from rpc import Server

HOST = '127.0.0.1'
PORT = 5000

server = Server(HOST, PORT)

if __name__ == '__main__':
    server.start()