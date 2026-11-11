def cycpattern_check(a, b):
    def is_rotation(s1, s2):
        if len(s1) != len(s2):
            return False
        return s2 in s1 + s1
    
    for i in range(len(b)):
        rotated_b = b[i:] + b[:i]
        if rotated_b in a:
            return True
    return False