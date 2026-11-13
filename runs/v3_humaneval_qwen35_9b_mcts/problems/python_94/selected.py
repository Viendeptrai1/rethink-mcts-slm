import math

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.sqrt(n)) + 1
    for i in range(3, sqrt_n, 2):
        if n % i == 0:
            return False
    return True

def skjkasdkd(lst):
    for num in sorted(lst, reverse=True):
        if is_prime(num):
            digit_sum = sum(int(d) for d in str(num))
            return digit_sum
    return 0