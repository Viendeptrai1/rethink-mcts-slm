def any_int(x, y, z):
    # Check if all numbers are integers
    if isinstance(x, int) and isinstance(y, int) and isinstance(z, int):
        # Check if one of the numbers is equal to the sum of the other two
        if x == y + z or y == x + z or z == x + y:
            return True
    return False

# Test cases
print(any_int(5, 2, 7))  # ➞ True
print(any_int(3, 2, 2))  # ➞ False
print(any_int(3, -2, 1))  # ➞ True
print(any_int(3.6, -2.2, 2))  # ➞ False