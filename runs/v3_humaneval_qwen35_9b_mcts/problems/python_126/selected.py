def is_sorted(lst):
    if not lst:
        return True
    
    # Track frequency of each number
    freq = {}
    
    # First pass: check for duplicates > 2 and build frequency map
    for num in lst:
        freq[num] = freq.get(num, 0) + 1
        if freq[num] > 2:
            return False
    
    # Second pass: check if sorted in ascending order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    
    return True