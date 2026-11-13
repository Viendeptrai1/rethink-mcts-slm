def iscube(a):
    if a == 0:
        return True
    if a > 0:
        root = int(round(a ** (1/3)))
        return root ** 3 == a
    else:
        root = int(round((-a) ** (1/3)))
        return (-root) ** 3 == a