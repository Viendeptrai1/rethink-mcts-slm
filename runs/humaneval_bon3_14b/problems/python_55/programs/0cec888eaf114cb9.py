def fib(n: int) -> int:
    """Return n-th Fibonacci number."""
    if n <= 0:
        raise ValueError("n must be a positive integer")
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        a, b = 1, 1
        for _ in range(2, n):
            a, b = b, a + b
        return b

# Test cases
print(fib(10))  # Output: 55
print(fib(1))   # Output: 1
print(fib(8))   # Output: 21