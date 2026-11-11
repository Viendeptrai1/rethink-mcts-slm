def fibfib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    # Initialize the base cases
    fibfib_values = [0, 0, 1]
    
    # Compute the sequence up to n using dynamic programming
    for i in range(3, n + 1):
        next_value = fibfib_values[i - 1] + fibfib_values[i - 2] + fibfib_values[i - 3]
        fibfib_values.append(next_value)
    
    return fibfib_values[n]