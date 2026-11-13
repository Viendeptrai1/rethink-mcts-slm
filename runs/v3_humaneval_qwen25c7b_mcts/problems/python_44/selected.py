def change_base(x: int, base: int) -> str:
    if x == 0:
        return "0"
    digits = []
    while x:
        digits.append(int(x % base))
        x //= base
    return ''.join(str(x) for x in digits[::-1])