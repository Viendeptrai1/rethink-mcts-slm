from collections import deque

def cycpattern_check(a, b):
    if len(b) > len(a):
        return False
    
    n = len(a)
    m = len(b)
    
    # Generate all rotations of b
    rotations = [b[i:] + b[:i] for i in range(m)]
    
    # Check if any rotation of b is a substring of a
    for rotation in rotations:
        if rotation in a:
            return True
            
    return False