import math

def sum_squares(lst):
    total = 0
    for num in lst:
        ceiling_val = math.ceil(num)
        total += ceiling_val ** 2
    return total