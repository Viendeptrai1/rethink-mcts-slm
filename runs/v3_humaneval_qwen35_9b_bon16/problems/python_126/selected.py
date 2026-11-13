def is_sorted(lst):
    if len(lst) <= 1:
        return True
    
    for i in range(1, len(lst)):
        if lst[i] < lst[i-1]:
            return False
        if lst[i] == lst[i-1]:
            # Check if this is the start of a sequence of more than 2 identical numbers
            count = 2
            j = i
            while j + 1 < len(lst) and lst[j + 1] == lst[j]:
                count += 1
                j += 1
            if count > 2:
                return False
    
    return True