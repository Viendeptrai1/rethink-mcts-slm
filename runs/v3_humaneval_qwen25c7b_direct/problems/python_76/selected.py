import math

def is_simple_power(x, n):
    if n == 1:
        return x == 1
    power = round(math.log(x, n))
    return n ** power == x