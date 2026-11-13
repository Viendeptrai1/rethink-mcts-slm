def cycpattern_check(a, b):
    if len(b) > len(a):
        return False
    
    for i in range(len(b)):
        rotation = b[i:] + b[:i]
        if rotation in a:
            return True
    
    return False