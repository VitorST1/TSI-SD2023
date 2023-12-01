from functools import reduce
from multiprocessing import Pool
import math
import os
import rpc.scrapping as scrapping
import concurrent.futures
import re

class Operations:
    @staticmethod
    def sum(*numbers):
        numbers = [float(x) for x in numbers]
        return reduce(lambda x, y: x + y, numbers)

    @staticmethod
    def div(*numbers):
        numbers = [float(x) for x in numbers]
        if 0 in numbers:
            return 0
        return reduce(lambda x, y: x / y, numbers)
    
    @staticmethod
    def mul(*numbers):
        numbers = [float(x) for x in numbers]
        return reduce(lambda x, y: x * y, numbers)

    @staticmethod
    def sub(*numbers):
        numbers = [float(x) for x in numbers]
        return reduce(lambda x, y: x - y, numbers)
    
    @staticmethod
    def is_prime(*numbers):
        numbers = [float(x) for x in numbers]
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
        number = float(number)
        if number > 1:
            for num in range(2, int(number**0.5) + 1):
                if number % num == 0:
                    return False
            return True
        return False
    
    @staticmethod
    def show_prime_in_range(*numbers):
        numbers = [float(x) for x in numbers]
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

    def valida_CPF(cpf):
        """ Efetua a validação do CPF, tanto formatação quando dígito verificadores.

        Parâmetros:
            cpf (str): CPF a ser validado

        Retorno:
            bool:
                - Falso, quando o CPF não possuir o formato 99999999999;
                - Falso, quando o CPF não possuir 11 caracteres numéricos;
                - Falso, quando os dígitos verificadores forem inválidos;
                - Verdadeiro, caso contrário.

        Exemplos:

        >>> valida_CPF('529.982.247-25')
        False
        >>> valida_CPF('52998224725')
        True
        >>> valida_CPF('111.111.111-11')
        False
        """

        # Verifica a formatação do CPF
        if not re.match(r'(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})', cpf):
            return False

        # Obtém apenas os números do CPF, ignorando pontuações
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        # Verifica se o CPF possui 11 números ou se todos são iguais:
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        # Validação do segundo dígito verificador:
        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
