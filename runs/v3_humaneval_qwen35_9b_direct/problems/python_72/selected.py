def will_it_fly(q, w):
    if not q:
        return False
    
    if sum(q) > w:
        return False
    
    return q == q[::-1]