def is_sorted(lst):
    if len(lst) <= 1:
        return True
    
    seen = set()
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1] or lst[i] in seen:
            return False
        seen.add(lst[i])
    
    return True