def cycpattern_check(a, b):
    # Check if b is a substring of a
    if b in a:
        return True
    
    # Generate all rotations of b
    for i in range(len(b)):
        rotated_b = b[i:] + b[:i]
        if rotated_b in a:
            return True
    
    return False

# Test cases
print(cycpattern_check("abcd", "abd"))  # False
print(cycpattern_check("hello", "ell"))  # True
print(cycpattern_check("whassup", "psus"))  # False
print(cycpattern_check("abab", "baa"))  # True
print(cycpattern_check("efef", "eeff"))  # False
print(cycpattern_check("himenss", "simen"))  # True