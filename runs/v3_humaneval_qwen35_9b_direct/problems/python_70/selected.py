def strange_sort_list(lst):
    if not lst:
        return []
    
    result = []
    sorted_lst = sorted(lst)
    left = 0
    right = len(sorted_lst) - 1
    
    while left <= right:
        if left == right:
            result.append(sorted_lst[left])
            break
        result.append(sorted_lst[left])
        left += 1
        result.append(sorted_lst[right])
        right -= 1
    
    return result