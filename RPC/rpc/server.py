import socket
from threading import Thread
import json
from rpc.operations import Operations
import datetime
import os
import ssl


class Server:
    def __init__(self, host, port):
        self.socketConnection = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = host
        self.PORT = port
        self.BUFFER = 1024
        self.LOG_FILENAME = os.path.join('.', 'logs', f'log{host}-{port}.txt')
        self.LOG_SEPARATOR = ','
        self.SSL_CONTEXT = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.SSL_CERTFILE = "./SSL/rootCA.pem"
        self.SSL_KEYFILE = "./SSL/rootCA.key"
        self.SSL_CONTEXT.load_cert_chain(
            certfile=self.SSL_CERTFILE, keyfile=self.SSL_KEYFILE)
        print(f'server running on port {port}')

    def __operationsHelper(self, operation, *params):
        return getattr(Operations, operation)(*params)

    def __getCaller(self, data):
        return data.split(' ')[0]

    def __getParams(self, data):
        params = []
        for n in data.split(' ')[1:]:
            params.append(n)

        return params

    def __dataHandler(self, data):
        caller = self.__getCaller(data)
        params = self.__getParams(data)

        return self.__operationsHelper(caller, *params)

    def __processData(self, conn):
        while True:  # loop to receive multiple messages from the client
            if (conn.fileno() == -1):  # means socket is closed
                break

            with self.SSL_CONTEXT.wrap_socket(conn, server_side=True) as secure_conn:
                data = secure_conn.recv(self.BUFFER).decode()

                if not data:
                    break

                startTime = datetime.datetime.now()
                response = self.__dataHandler(data)

                secure_conn.send(json.dumps({'resp': response}).encode())
                endTime = datetime.datetime.now()
                self.__generateLog(data, secure_conn.getpeername()
                                   [0], endTime - startTime)

    def __generateLog(self, data, clientIp, responseTime):
        timestamp = datetime.datetime.now()
        caller = self.__getCaller(data)
        log = f'{timestamp}{self.LOG_SEPARATOR}{clientIp}{self.LOG_SEPARATOR}{caller}{self.LOG_SEPARATOR}{responseTime.microseconds / 1000}\n'
        print(log)
        os.makedirs(os.path.dirname(self.LOG_FILENAME), exist_ok=True)
        with open(self.LOG_FILENAME, 'a', encoding='utf-8') as f:
            f.write(str(log))
            f.flush()

    def start(self):
        self.socketConnection.bind((self.HOST, self.PORT))
        self.socketConnection.listen()

        while True:  # loop to keep the server running after a client connection
            conn, address = self.socketConnection.accept()
            print("Connection from: " + str(address))

            thread = Thread(target=self.__processData, args=(conn,))

            thread.start()
