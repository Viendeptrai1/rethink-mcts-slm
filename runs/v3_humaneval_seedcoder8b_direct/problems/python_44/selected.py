def change_base(x: int, base: int) -> str:
    if x == 0:
        return '0'
    
    digits = []
    while x > 0:
        digits.append(str(x % base))
        x //= base
    
    return ''.join(digits[::-1])