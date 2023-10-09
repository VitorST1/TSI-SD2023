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
        self.SERVERS_FILENAME = './rpc/nameServer/servers.json'
        self.serversDict = {}

        # obtém os servidores em arquivo utilizado thread
        thread = Thread(target=self.getServersFromDisk)
        thread.start()

        print(f'server running on port {port}')
    
    def getServersFromDisk(self):
        try:
            with open(self.SERVERS_FILENAME) as f:
                servers = json.load(f)
        except Exception as e:
            servers = {}
            
        self.serversDict = servers

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