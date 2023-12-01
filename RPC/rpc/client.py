import socket
import json
import inspect
from rpc.cache import Cache
import random
import ssl


class Client:
    def __init__(self, host, port):
        self._SERVER_TRIES_LIMIT = 5
        self.__nameServerConnection = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)
        # self.nameServerTimeoutCount = 0
        self.__NAME_SERVER_TIMEOUT = 100
        self.HOST = host
        self.PORT = port
        self.__BUFFER = 1024
        self.__cache = Cache()
        self.SSL_CONTEXT = ssl.create_default_context()
        self.SSL_CONTEXT.load_verify_locations("./SSL/device.crt")
        self.SSL_CONTEXT.check_hostname = False
        self.SSL_CONTEXT.verify_mode = ssl.CERT_NONE

    def __helper(self, params):
        caller = inspect.stack()[1].function
        task = f"{caller} {' '.join(map(str, params))}"

        cache = self.__cache.getFromMemory(task)

        if (cache != None):
            print('getting from cache')
            return cache
        else:
            servers = self.__getOperationServer(caller)
            if servers and len(servers):
                excludeServer = None
                serverTriesCount = 0
                while True:
                    if serverTriesCount >= self._SERVER_TRIES_LIMIT:
                        return self.__returnError(caller, f'Server unavailable for operation {caller}')

                    serverHost, serverPort = self.__pickServer(
                        servers, excludeServer)

                    if serverHost and serverPort:
                        print(
                            f'getting "{caller}" from server {serverHost}:{serverPort}')
                        try:
                            resp = self.__getInServer(
                                task, serverHost, serverPort)
                            return resp

                        except Exception as e:
                            print('here', e)
                            if (len(servers) > 1):
                                excludeServer = [serverHost, serverPort]
                            serverTriesCount += 1
                            pass
        return self.__returnError(caller, 'Server unavailable')

    def __getOperationServer(self, operation):
        self.__nameServerConnection.settimeout(self.__NAME_SERVER_TIMEOUT)
        self.__nameServerConnection.sendto(
            operation.encode(), (self.HOST, self.PORT))

        try:
            data = self.__nameServerConnection.recv(self.__BUFFER)
            data = json.loads(data.decode())['resp']
            self.nameServerTimeoutCount = 0
            return data
        except:
            return

    def __pickServer(self, servers, excludeServer):
        if (excludeServer):
            available_servers = [
                server for server in servers if server != excludeServer]
            server = random.choice(available_servers)
        else:
            server = random.choice(servers)
        return server

    def __getInServer(self, task, serverHost, serverPort):
        self.serverConnection = self.SSL_CONTEXT.wrap_socket(socket.socket(
            socket.AF_INET, socket.SOCK_STREAM), server_hostname=serverHost)

        self.serverConnection.connect((serverHost, serverPort))
        print('task', task)
        self.serverConnection.send(task.encode())
        data = bytearray()

        while True:
            aux = self.serverConnection.recv(self.__BUFFER)

            if not aux:
                break

            data += aux

            if len(aux) < self.__BUFFER:
                break

        print('data', data)
        data = json.loads(data.decode())['resp']

        self.__cache.write(task, data)
        self.serverConnection.close()

        return data

    def __returnError(self, operation, message):
        return [message] if self.__operationReturnIsArray(operation) else message

    def __operationReturnIsArray(self, operation):
        if operation == 'last_news_if_barbacena' or operation == 'show_prime_in_range' or operation == 'show_prime_in_range_multiprocessing' or operation == 'is_prime':
            return True
        return False

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

    def valida_CPF(self, cpf):
        return self.__helper((cpf, ))

    def close(self):
        self.__cache.writeInDisk()
