def iscube(a):
    if a == 0:
        return True
    if a > 0:
        n = 1
        while n ** 3 < a:
            n += 1
        return n ** 3 == a
    else:
        n = 1
        while -(n ** 3) > a:
            n += 1
        return -(n ** 3) == a