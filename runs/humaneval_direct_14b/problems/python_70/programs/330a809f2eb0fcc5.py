def strange_sort_list(lst):
    sorted_lst = sorted(lst)
    result = []
    left, right = 0, len(sorted_lst) - 1
    while left <= right:
        if left == right:
            result.append(sorted_lst[left])
        else:
            result.append(sorted_lst[left])
            result.append(sorted_lst[right])
        left += 1
        right -= 1
    return result

# Test cases
print(strange_sort_list([1, 2, 3, 4]))  # Output: [1, 4, 2, 3]
print(strange_sort_list([5, 5, 5, 5]))  # Output: [5, 5, 5, 5]
print(strange_sort_list([]))            # Output: []