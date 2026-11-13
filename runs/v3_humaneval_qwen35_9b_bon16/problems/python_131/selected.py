def digits(n: int) -> int:
    product = 1
    found_odd = False
    for char in str(n):
        digit = int(char)
        if digit % 2 == 1:
            product *= digit
            found_odd = True
    return 0 if not found_odd else product