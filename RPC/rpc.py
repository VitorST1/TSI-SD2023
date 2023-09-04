import socket
import inspect
from functools import reduce
import math
from multiprocessing import Pool
import os

class Client:
    __cache_dict = {}

    def __init__(self, host, port):
        self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.connect((host, port))
        self.BUFFER = 1024

    def __getInCache(self, task):
        if task in self.__cache_dict:
            return self.__cache_dict[task]
        else:
            return None
        
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

        self.__cache_dict[task] = data # add task result to cache

        return data

    def __helper(self, numbers):
        caller = inspect.stack()[1].function

        task = f"{caller} {' '.join(map(str, numbers))}"

        cache = self.__getInCache(task)

        if(cache != None):
            print('got from cache')
            return cache.decode()
        else:
            print('got from server')
            return self.__getInServer(task).decode()
        
        

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
    
    def close(self):
        self.socketConnection.close()


class NumberUtils:
    @staticmethod
    def is_prime(*numbers):
        primes = []
        
        for num in numbers:
            if num < 2: # Numbers less than 2 are not prime
                primes.append(False)
            else:
                is_prime = True
                for i in range(2, int(math.sqrt(num)) + 1):
                    if num % i == 0:
                        is_prime = False
                        break
                
                primes.append(is_prime)
        
        return primes
        
    @staticmethod
    def number_is_prime(number):
        if number > 1:
            for num in range(2, int(number**0.5) + 1):
                if number % num == 0:
                    return False
            return True
        return False
    
    @staticmethod
    def show_prime_in_range(*numbers):
        begin, end = map(int, numbers)

        ret = []

        for n in range(begin, end):
            if(NumberUtils.is_prime(n)[0]):
                ret.append(n)

        return ret
    
    @staticmethod
    def show_prime_in_range_multiprocessing(begin, end):
        begin = int(begin)
        end = int(end)

        with Pool(processes=os.cpu_count()) as pool:
            numbers = range(begin, end + 1)
            prime_flags = pool.map(NumberUtils.number_is_prime, numbers)
            prime_numbers = [number[0] for number in zip(numbers, prime_flags) if number [1]]
        
        return prime_numbers


class Operations:
    @staticmethod
    def sum(*numbers):
        return reduce(lambda x, y: x + y, numbers)

    @staticmethod
    def div(*numbers):
        if numbers.__contains__(0):
            return 0
        return reduce(lambda x, y: x / y, numbers)
    
    @staticmethod
    def mul(*numbers):
        return reduce(lambda x, y: x * y, numbers)

    @staticmethod
    def sub(*numbers):
        return reduce(lambda x, y: x - y, numbers)
    
class Server:
        def __init__(self, host, port):
            self.socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketConnection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.HOST = host
            self.PORT = port
            self.BUFFER = 1024
        
        def __operationsHelper(self, operation, *numbers):
            return getattr(Operations, operation)(*numbers)
        
        def __numberUtilsHelper(self, method, *numbers):
            return getattr(NumberUtils, method)(*numbers)

        def __getCaller(self, data):
            return data.split(' ')[0]
        
        def __getNumbers(self, data):
            numbers = []
            for n in data.split(' ')[1:]:
                numbers.append(float(n))

            return numbers
        
        def __isOperation(self, caller):
            operations = (
                'sum',
                'mul',
                'div',
                'sub'
            )

            if operations.__contains__(caller):
                return True
            
            return False

        def __dataHandler(self, data):
            caller = self.__getCaller(data)
            if(self.__isOperation(caller)):
                numbers = self.__getNumbers(data)
                return self.__operationsHelper(caller, *numbers)
            else:
                numbers = self.__getNumbers(data)
                return self.__numberUtilsHelper(caller, *numbers)

        def start(self):
            self.socketConnection.bind((self.HOST, self.PORT))
            self.socketConnection.listen()
            
            while True: # loop to keep the server running after a client connection
                conn, address = self.socketConnection.accept()
                print("Connection from: " + str(address))

                while True: # loop to receive multiple messages from the client
                    data = conn.recv(self.BUFFER).decode()

                    if not data:
                        break

                    ret = str(self.__dataHandler(data))

                    conn.send(ret.encode())