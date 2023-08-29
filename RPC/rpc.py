import socket
import inspect
from functools import reduce

class Client:
    def __init__(self, host, port):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.connect((host, port))
        self.BUFFER = 1048

    def __socketHelper(self, numbers):
        caller = inspect.stack()[1].function
        
        self.socketConnection.send(f"{caller} {' '.join(map(str, numbers))}".encode())

        return self.socketConnection.recv(self.BUFFER).decode()

    def sum(self, *numbers):
        return self.__socketHelper(numbers)

    def div(self, *numbers):
        return self.__socketHelper(numbers)

    def mul(self, *numbers):
        return self.__socketHelper(numbers)

    def sub(self, *numbers):
        return self.__socketHelper(numbers)
    
    def close(self):
        self.socketConnection.close()

class Operations:
    def sum(self, *numbers):
        return reduce(lambda x, y: x + y, numbers)

    def div(self, *numbers):
        if numbers.__contains__(0):
            return 0
        return reduce(lambda x, y: x / y, numbers)

    def mul(self, *numbers):
        return reduce(lambda x, y: x * y, numbers)

    def sub(self, *numbers):
        return reduce(lambda x, y: x - y, numbers)
    
class Server:
        def __init__(self, host, port):
            self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketConnection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.HOST = host
            self.PORT = port
            self.BUFFER = 1024
            self.operations = Operations()

        def __operationsHelper(self, operation, *numbers):
            return getattr(self.operations, operation)(*numbers)

        def __getCaller(self, data):
            return data.split(' ')[0]
        
        def __getNumbers(self, data):
            numbers = []
            for n in data.split(' ')[1:]:
                numbers.append(float(n))

            return numbers

        def __dataHandler(self, data):
            operation = self.__getCaller(data)
            numbers = self.__getNumbers(data)
            return self.__operationsHelper(operation, *numbers)

        def start(self):
            self.socketConnection.bind((self.HOST, self.PORT))
            self.socketConnection.listen()
            
            while True: # loop to keep the server running after a client connection
                conn, address = self.socketConnection.accept()
                print("Connection from: " + str(address))

                while True: # loop to receive more than one message from the client
                    data = conn.recv(self.BUFFER).decode()

                    if not data:
                        break

                    ret = str(self.__dataHandler(data))

                    conn.send(ret.encode())


            

            