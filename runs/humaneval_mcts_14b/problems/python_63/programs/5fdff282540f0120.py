def fibfib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1

    # Initialize the first three numbers in the sequence
    a, b, c = 0, 0, 1

    # Compute the sequence iteratively
    for i in range(3, n + 1):
        next_value = a + b + c
        a, b, c = b, c, next_value

    return c

# Test cases
print(fibfib(1))  # Output: 0
print(fibfib(5))  # Output: 4
print(fibfib(8))  # Output: 24