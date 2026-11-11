def change_base(x: int, base: int) -> str:
    if x == 0:
        return "0"
    
    digits = []
    while x > 0:
        digits.append(str(x % base))
        x //= base
    
    return ''.join(reversed(digits))

# Example usage:
# print(change_base(8, 3))  # Output: '22'
# print(change_base(8, 2))  # Output: '1000'
# print(change_base(7, 2))  # Output: '111'