def digits(n):
    """Given a positive integer n, return the product of the odd digits.
    Return 0 if all digits are even.
    """
    product = 1
    has_odd = False
    while n > 0:
        digit = n % 10
        if digit % 2 != 0:
            product *= digit
            has_odd = True
        n //= 10
    return product if has_odd else 0