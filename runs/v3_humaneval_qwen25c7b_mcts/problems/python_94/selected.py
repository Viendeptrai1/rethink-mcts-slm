from math import sqrt

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def skjkasdkd(lst):
    max_prime = 0
    for num in lst:
        if num > max_prime and is_prime(num):
            max_prime = num
    
    return sum(int(digit) for digit in str(max_prime))