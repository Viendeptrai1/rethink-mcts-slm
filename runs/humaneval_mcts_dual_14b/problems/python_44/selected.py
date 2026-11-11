def change_base(x: int, base: int) -> str:
    if x == 0:
        return "0"
    
    digits = []
    while x > 0:
        remainder = x % base
        digits.append(str(remainder))
        x = x // base
    
    # The remainders are collected in reverse order
    digits.reverse()
    
    return ''.join(digits)