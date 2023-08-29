# client.py

from rpc import Client

client = Client('127.0.0.1', 5000)

print(client.sum(1.5, 50))

print(client.div(10, 0))

print(client.mul(5, 0))

print(client.sub(10, 12.5))

client.close()