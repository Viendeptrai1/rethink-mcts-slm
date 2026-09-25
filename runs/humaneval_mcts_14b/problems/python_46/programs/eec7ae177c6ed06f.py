def fib4(n: int) -> int:
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 2
    elif n == 3:
        return 0
    
    # Initialize the first four values of the sequence
    fib4_values = [0, 0, 2, 0]
    
    # Compute the sequence iteratively from 4 to n
    for i in range(4, n + 1):
        next_value = sum(fib4_values)
        # Update the list to hold the last four values
        fib4_values = fib4_values[1:] + [next_value]
    
    return fib4_values[-1]

# Test cases
print(fib4(5))  # Output: 4
print(fib4(6))  # Output: 8
print(fib4(7))  # Output: 14