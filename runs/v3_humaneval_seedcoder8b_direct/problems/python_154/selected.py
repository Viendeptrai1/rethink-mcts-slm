def cycpattern_check(a, b):
    if len(b) > len(a):
        return False
    
    double_a = a + a
    for i in range(len(a)):
        if double_a[i:i+len(b)] == b or double_a[i:i+len(b)][::-1] == b:
            return True
    
    return False