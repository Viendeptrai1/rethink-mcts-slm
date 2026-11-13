from math import ceil

def sum_squares(lst):
    return sum(int(ceil(num))**2 for num in lst)