def sum_squares(lst):
    import math
    return sum(math.ceil(x) ** 2 for x in lst)