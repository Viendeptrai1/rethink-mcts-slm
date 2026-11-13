def strange_sort_list(lst):
    lst.sort()
    result = []
    left, right = 0, len(lst) - 1
    while left <= right:
        if left == right:
            result.append(lst[left])
        else:
            result.extend([lst[left], lst[right]])
        left += 1
        right -= 1
    return result