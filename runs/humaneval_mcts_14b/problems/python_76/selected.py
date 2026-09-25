def is_simple_power(x, n):
    if n == 1:
        return x == 1
    if x < 1 or n < 1:
        return False
    power = 1
    while power < x:
        power *= n
    return power == x