def change_base(x: int, base: int) -> str:
    if base < 2 or base > 9:
        raise ValueError("Base must be between 2 and 9")
    
    if x == 0:
        return "0"
    
    digits = []
    while x > 0:
        digits.append(str(x % base))
        x //= base
    
    return "".join(digits[::-1])