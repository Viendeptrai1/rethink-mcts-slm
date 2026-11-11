def cycpattern_check(a, b):
    if len(b) > len(a):
        return False
    doubled_b = b + b
    return any(doubled_b[i:i+len(b)] in a for i in range(len(b)))