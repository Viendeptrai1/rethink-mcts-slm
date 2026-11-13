def iscube(a):
    if a == 0:
        return True
    
    abs_a = abs(a)
    i = 1
    while i * i * i <= abs_a:
        if i * i * i == abs_a:
            return True
        i += 1
    
    return False