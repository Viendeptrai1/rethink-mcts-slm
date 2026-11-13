def digits(n):
    product = 1
    has_odd = False
    for digit in str(n):
        int_digit = int(digit)
        if int_digit % 2 != 0:
            product *= int_digit
            has_odd = True
    return product if has_odd else 0