import math

def x_or_y(n, x, y):
    if n <= 1:
        return y
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return y
    return x