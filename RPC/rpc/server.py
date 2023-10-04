import socket
from threading import Thread
import json
from rpc.operations import Operations
    
class Server:
    def __init__(self, host, port):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = host
        self.PORT = port
        self.BUFFER = 1024
        print(f'server running on port {port}')
    
    def __operationsHelper(self, operation, *params):
        return getattr(Operations, operation)(*params)

    def __getCaller(self, data):
        return data.split(' ')[0]
    
    def __getParams(self, data):
        params = []
        for n in data.split(' ')[1:]:
            params.append(float(n))

        return params

    def __dataHandler(self, data):
        caller = self.__getCaller(data)
        params = self.__getParams(data)

        return self.__operationsHelper(caller, *params)
        
    def __processData(self, conn):
        while True: # loop to receive multiple messages from the client
            data = conn.recv(self.BUFFER).decode()

            if not data:
                break

            response = self.__dataHandler(data)

            conn.send(json.dumps({'resp': response}).encode())

    def start(self):
        self.socketConnection.bind((self.HOST, self.PORT))
        self.socketConnection.listen()
        
        while True: # loop to keep the server running after a client connection
            conn, address = self.socketConnection.accept()
            print("Connection from: " + str(address))

            thread = Thread(target=self.__processData, args=(conn,))

            thread.start()