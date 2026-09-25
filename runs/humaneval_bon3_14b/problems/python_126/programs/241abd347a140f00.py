def is_sorted(lst):
    if len(lst) <= 1:
        return True
    
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            return False
        if i > 1 and lst[i] == lst[i - 1] == lst[i - 2]:
            return False
    
    return True

# Test cases
print(is_sorted([5]))  # ➞ True
print(is_sorted([1, 2, 3, 4, 5]))  # ➞ True
print(is_sorted([1, 3, 2, 4, 5]))  # ➞ False
print(is_sorted([1, 2, 3, 4, 5, 6]))  # ➞ True
print(is_sorted([1, 2, 3, 4, 5, 6, 7]))  # ➞ True
print(is_sorted([1, 3, 2, 4, 5, 6, 7]))  # ➞ False
print(is_sorted([1, 2, 2, 3, 3, 4]))  # ➞ True
print(is_sorted([1, 2, 2, 2, 3, 4]))  # ➞ False