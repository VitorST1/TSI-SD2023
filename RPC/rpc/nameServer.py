import socket
import json
from threading import Thread

class NameServer:
    def __init__(self, host, port) -> None:
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socketConnection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = host
        self.PORT = port
        self.BUFFER = 1024
        self.serversDict = {
            'sum': [( '127.0.0.1', 6001 )],
            'sub': [( '127.0.0.1', 6001 )],
            'mul': [( '127.0.0.1', 6001 )],
            'div': [( '127.0.0.1', 6001 )],
            'is_prime': [( '127.0.0.1', 6002 )],
            'show_prime_in_range': [( '127.0.0.1', 6002 )],
            'mp_show_prime_in_range': [( '127.0.0.1', 6002 )],
            'last_news_if_barbacena': [( '127.0.0.1', 6003 ), ( '127.0.0.1', 6004 )],
        }
        print(f'server running on port {port}')

    def start(self):
        self.socketConnection.bind((self.HOST, self.PORT))
        
        while True: # loop to keep the server running after a client connection
            operation, address = self.socketConnection.recvfrom(self.BUFFER)
            print("Connection from: " + str(address), operation)

            data = (
                operation.decode(),
                address
            )

            thread = Thread(target=self.__processData, args=(data,))

            thread.start()

    def __processData(self, data):
        response = self.__serverHelper(data[0])
        self.socketConnection.sendto(json.dumps({'resp': response}).encode(), data[1])
    
    def __serverHelper(self, operation):
        if operation in self.serversDict:
            return self.serversDict[operation]