def iscube(a):
    if a == 0:
        return True
    sign = 1 if a > 0 else -1
    root = round(abs(a) ** (1/3))
    return (root ** 3 == abs(a)) and (sign == 1 or root != 0)