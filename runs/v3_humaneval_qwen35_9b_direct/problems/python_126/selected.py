def is_sorted(lst):
    if len(lst) <= 1:
        return True
    
    # Check for duplicates first
    if len(lst) != len(set(lst)):
        return False
    
    # Check if sorted in ascending order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    
    return True