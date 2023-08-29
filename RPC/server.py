# server.py

from rpc import Server

server = Server('127.0.0.1', 5000)

if __name__ == '__main__':
    server.start()