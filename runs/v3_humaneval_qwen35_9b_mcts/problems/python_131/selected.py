def digits(n):
    product = 1
    found_odd = False
    for ch in str(n):
        digit = int(ch)
        if digit % 2 == 1:
            product *= digit
            found_odd = True
    return product if found_odd else 0