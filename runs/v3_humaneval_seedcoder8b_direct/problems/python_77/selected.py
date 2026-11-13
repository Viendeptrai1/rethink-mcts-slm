def iscube(a):
    if a == 0:
        return True
    abs_a = abs(a)
    cube_root = round(abs_a ** (1/3))
    return cube_root ** 3 == abs_a