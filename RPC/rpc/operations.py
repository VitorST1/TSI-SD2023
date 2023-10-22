from functools import reduce
from multiprocessing import Pool
import math
import os
import rpc.scrapping as scrapping
import concurrent.futures

class Operations:
    @staticmethod
    def sum(*numbers):
        return reduce(lambda x, y: x + y, numbers)

    @staticmethod
    def div(*numbers):
        if 0 in numbers:
            return 0
        return reduce(lambda x, y: x / y, numbers)
    
    @staticmethod
    def mul(*numbers):
        return reduce(lambda x, y: x * y, numbers)

    @staticmethod
    def sub(*numbers):
        return reduce(lambda x, y: x - y, numbers)
    
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
            if(Operations.is_prime(n)[0]):
                ret.append(n)

        return ret
    
    @staticmethod
    def show_prime_in_range_multiprocessing(begin, end):
        begin = int(begin)
        end = int(end)

        with Pool(processes=os.cpu_count()) as pool:
            numbers = range(begin, end + 1)
            prime_flags = pool.map(Operations.number_is_prime, numbers)
            prime_numbers = [number[0] for number in zip(numbers, prime_flags) if number [1]]
        
        return prime_numbers
    
    @staticmethod
    def last_news_if_barbacena(newsCount):
        newsCount = int(newsCount)
        perPage = 20
        pages = math.ceil(newsCount / perPage)

        resp = []

        urls = []
        for i in range(pages):
            url = f'ifsudestemg.edu.br/noticias/barbacena/?b_start:int={ perPage * (i)} '
            urls.append(url)

        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for n in executor.map(scrapping.get_links, urls):
                if not n:
                    break
                resp += n
        
        resp = resp[0:newsCount]

        return resp