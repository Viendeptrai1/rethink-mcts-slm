def cycpattern_check(a, b):
    n = len(b)
    rotations = [b[i:] + b[:i] for i in range(n)]
    return any(rot in a for rot in rotations)