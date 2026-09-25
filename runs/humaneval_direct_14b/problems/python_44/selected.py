def change_base(x: int, base: int) -> str:
    if base < 2 or base > 9:
        raise ValueError("Base must be between 2 and 9, inclusive.")
    
    if x == 0:
        return "0"
    
    digits = []
    while x > 0:
        remainder = x % base
        digits.append(str(remainder))
        x = x // base
    
    # The digits are collected in reverse order
    digits.reverse()
    
    return ''.join(digits)

# Test cases
print(change_base(8, 3))  # Output: '22'
print(change_base(8, 2))  # Output: '1000'
print(change_base(7, 2))  # Output: '111'