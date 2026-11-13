import math

def is_simple_power(x, n):
    if n == 1:
        return x == 1
    log_result = math.log(x, n)
    return log_result.is_integer()