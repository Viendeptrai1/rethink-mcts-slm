def fibfib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    # Initialize the base cases
    fibfib_values = [0, 0, 1]
    
    # Compute the sequence iteratively up to n
    for i in range(3, n + 1):
        next_value = fibfib_values[i - 1] + fibfib_values[i - 2] + fibfib_values[i - 3]
        fibfib_values.append(next_value)
    
    return fibfib_values[n]

# Test cases
print(fibfib(1))  # Output: 0
print(fibfib(5))  # Output: 4
print(fibfib(8))  # Output: 24