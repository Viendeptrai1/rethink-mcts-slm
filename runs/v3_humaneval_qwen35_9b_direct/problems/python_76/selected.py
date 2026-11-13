def is_simple_power(x, n):
    if x == 1:
        return True
    if n == 1:
        return False
    if x <= 0:
        return False
    if n <= 0:
        return False
    
    current = n
    while current < x:
        current *= n
        if current < 0:
            return False
    return current == x