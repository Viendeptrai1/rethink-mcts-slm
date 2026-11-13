def cycpattern_check(a, b):
    if len(b) > len(a):
        return False
    
    rotations = [b[i:] + b[:i] for i in range(len(b))]
    
    for rotation in rotations:
        if rotation in a:
            return True
    
    return False