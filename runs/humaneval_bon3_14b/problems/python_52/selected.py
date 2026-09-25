def below_threshold(l: list, t: int) -> bool:
    """Return True if all numbers in the list l are below threshold t."""
    return all(x < t for x in l)

# Test cases
print(below_threshold([1, 2, 4, 10], 100))  # Expected output: True
print(below_threshold([1, 20, 4, 10], 5))   # Expected output: False