def is_simple_power(x, n):
    if x == 1:
        return True
    if n == 1:
        return False
    current = n
    while current < x:
        current *= n
    return current == x