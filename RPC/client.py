# client.py

from rpc.client import Client
import time

HOST = 'localhost'
PORT = 5000

client = Client(HOST, PORT)

# print(f'Soma: {client.sum(1.5, 500)}')

print(f'Div: {client.div(10, 2)}')

# # # time.sleep(3)

# print(f'Mul: {client.mul(5, 0)}')

# print(f'Sub: {client.sub(10, 12.5)}')

# print(client.is_prime(13, 11, 2))

# array = client.last_news_if_barbacena(2) # number of news
# for title in array:
#     print(title)


# time.sleep(5 * 60)
# time.sleep(1)
# array = client.last_news_if_barbacena(900000)  # number of news
# for title in array:
#     print(title)

# start = time.time()
# client.show_prime_in_range(10, 1000000)
# # print(client.show_prime_in_range(10, 100000))
# end = time.time()
# print(str(end - start) + '\n')

# start = time.time()
# client.show_prime_in_range_multiprocessing(10, 1000000)
# print(client.show_prime_in_range_multiprocessing(10, 100))
# end = time.time()
# print(str(end - start) + '\n')

# print(f'Valida CPF: {client.valida_CPF("53002666807")}')

client.close()
