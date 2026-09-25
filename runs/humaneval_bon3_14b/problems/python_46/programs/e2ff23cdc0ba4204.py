def fib4(n: int) -> int:
    if n == 0 or n == 1 or n == 3:
        return 0
    elif n == 2:
        return 2
    
    # Initialize the first four elements of the sequence
    fib4_values = [0, 0, 2, 0]
    
    # Compute the sequence iteratively up to the n-th element
    for i in range(4, n + 1):
        next_value = sum(fib4_values[-4:])
        fib4_values.append(next_value)
    
    return fib4_values[n]

# Test cases
print(fib4(5))  # Output: 4
print(fib4(6))  # Output: 8
print(fib4(7))  # Output: 14