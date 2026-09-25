def modp(n: int, p: int) -> int:
    """Return 2^n modulo p (be aware of numerics)."""
    return pow(2, n, p)

# Test cases
print(modp(3, 5))    # Output: 3
print(modp(1101, 101))  # Output: 2
print(modp(0, 101))    # Output: 1
print(modp(3, 11))   # Output: 8
print(modp(100, 101))  # Output: 1