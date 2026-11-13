def next_smallest(lst):
    if len(lst) < 2:
        return None
    
    # Sort the list to find the smallest and second smallest
    sorted_lst = sorted(lst)
    
    # Check if the second element is different from the first
    if sorted_lst[0] != sorted_lst[1]:
        return sorted_lst[1]
    else:
        return None