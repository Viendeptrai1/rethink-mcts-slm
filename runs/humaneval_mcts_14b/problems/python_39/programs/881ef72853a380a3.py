from sympy import isprime

def prime_fib(n: int) -> int:
    """
    prime_fib returns n-th number that is a Fibonacci number and it's also prime.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    fib1, fib2 = 1, 1
    count = 0
    
    while True:
        fib_next = fib1 + fib2
        fib1, fib2 = fib2, fib_next
        
        if isprime(fib_next):
            count += 1
            if count == n:
                return fib_next

# Test cases
print(prime_fib(1))  # Output: 2
print(prime_fib(2))  # Output: 3
print(prime_fib(3))  # Output: 5
print(prime_fib(4))  # Output: 13
print(prime_fib(5))  # Output: 89