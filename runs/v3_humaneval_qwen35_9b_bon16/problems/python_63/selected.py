def fibfib(n: int):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    
    a, b, c = 0, 0, 1  # fibfib(0), fibfib(1), fibfib(2)
    
    for i in range(3, n + 1):
        next_val = a + b + c
        a, b, c = b, c, next_val
        
    return c