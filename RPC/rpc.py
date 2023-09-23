import socket
import inspect
from cache import Cache
from threading import Thread
import json
from operations import Operations

class Client:
    def __init__(self, host, port):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.connect((host, port))
        self.BUFFER = 1024
        self.cache = Cache()
        
    def __getInServer(self, task):
        self.socketConnection.send(task.encode())
        
        data = bytearray()

        while True:
            aux = self.socketConnection.recv(self.BUFFER)

            if not aux:
                break

            data += aux

            if len(aux) < self.BUFFER:
                break

        data = json.loads(data.decode())['resp']

        self.cache.write(task, data)

        return data

    def __helper(self, params):
        caller = inspect.stack()[1].function

        task = f"{caller} {' '.join(map(str, params))}"

        cache = self.cache.getFromMemory(task)

        if(cache != None):
            print('getting from cache')
            return cache
        else:
            print('getting from server')
            return self.__getInServer(task)
        
    def sum(self, *numbers):
        return self.__helper(numbers)

    def div(self, *numbers):
        return self.__helper(numbers)

    def mul(self, *numbers):
        return self.__helper(numbers)

    def sub(self, *numbers):
        return self.__helper(numbers)
    
    def is_prime(self, *numbers):
        return self.__helper(numbers)
    
    def show_prime_in_range(self, begin, end):
        return self.__helper((begin, end))
    
    def show_prime_in_range_multiprocessing(self, begin, end):
        return self.__helper((begin, end))
    
    def last_news_if_barbacena(self, newsCount):
        return self.__helper((newsCount, ))
    
    def close(self):
        self.cache.writeInDisk()
        self.socketConnection.close()
    
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

