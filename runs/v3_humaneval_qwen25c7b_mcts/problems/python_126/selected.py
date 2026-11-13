def is_sorted(lst):
    if len(lst) <= 1:
        return True
    
    prev = lst[0]
    duplicate_count = 0
    
    for num in lst[1:]:
        if num < prev:
            return False
        if num == prev:
            duplicate_count += 1
            if duplicate_count > 1:
                return False
        else:
            duplicate_count = 0
        prev = num
    
    return True