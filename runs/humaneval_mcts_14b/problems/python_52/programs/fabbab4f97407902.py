def below_threshold(l: list, t: int) -> bool:
    for num in l:
        if num >= t:
            return False
    return True

# Test cases
print(below_threshold([1, 2, 4, 10], 100))  # Expected output: True
print(below_threshold([1, 20, 4, 10], 5))   # Expected output: False