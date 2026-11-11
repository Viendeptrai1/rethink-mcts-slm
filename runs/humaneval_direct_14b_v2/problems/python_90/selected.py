def next_smallest(lst):
    if len(lst) < 2:
        return None
    
    first, second = float('inf'), float('inf')
    
    for num in lst:
        if num < first:
            first, second = num, first
        elif first < num < second:
            second = num
    
    return second if second != float('inf') else None