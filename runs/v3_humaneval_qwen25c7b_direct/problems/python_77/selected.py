import math

def iscube(a):
    if a == 0:
        return True
    abs_a = abs(a)
    root = round(abs_a ** (1/3))
    return root ** 3 == abs_a