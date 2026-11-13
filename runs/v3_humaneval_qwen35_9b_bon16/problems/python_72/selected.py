def will_it_fly(q, w):
    if not isinstance(q, list):
        q = [q]
    
    if q == q[::-1]:
        if sum(q) <= w:
            return True
    return False