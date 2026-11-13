def closest_integer(value):
    num = float(value)
    # Round away from zero using floor division and add a condition
    return int(num + 0.5) if num > 0 else int(num - 0.5)

# Test cases
print(closest_integer("10"))    # Output: 10
print(closest_integer("15.3"))  # Output: 15
print(closest_integer("14.5"))  # Output: 15
print(closest_integer("-14.5")) # Output: -15