def fib4(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n == 2:
        return 2
    if n == 3:
        return 0
    
    # Initialize the first four values
    a, b, c, d = 0, 0, 2, 0
    
    # Iterate from 4 to n
    for _ in range(4, n + 1):
        next_val = a + b + c + d
        a, b, c, d = b, c, d, next_val
    
    return d