def digits(n):
    product = 1
    has_odd = False
    for digit_char in str(n):
        digit = int(digit_char)
        if digit % 2 == 1:
            product *= digit
            has_odd = True
    return product if has_odd else 0