# client.py

from rpc import Client
import time

client = Client('127.0.0.1', 5000)

print(client.sum(1.5, 50))

print(client.div(10, 0))

# time.sleep(3)

print(client.mul(5, 0))

# print(client.sub(10, 12.5))

# print(client.is_prime(13, 13, 13, 13, 13, 13, 11, 9999992))

# start = time.time()
# client.show_prime_in_range(10, 1000000)
# # print(client.show_prime_in_range(10, 100000))
# end = time.time()
# print(str(end - start) + '\n')

# start = time.time()
# client.show_prime_in_range(10, 1000000)
# # print(client.show_prime_in_range(10, 100000))
# end = time.time()
# print(str(end - start) + '\n')

# start = time.time()
# client.show_prime_in_range_multiprocessing(10, 1000000)
# # print(client.show_prime_in_range_multiprocessing(10, 100000))
# end = time.time()
# print(str(end - start) + '\n')

client.close()