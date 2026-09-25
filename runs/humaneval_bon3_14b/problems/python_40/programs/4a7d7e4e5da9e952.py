def triples_sum_to_zero(l: list) -> bool:
    n = len(l)
    if n < 3:
        return False
    
    l.sort()
    
    for i in range(n - 2):
        if i > 0 and l[i] == l[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        while left < right:
            total = l[i] + l[left] + l[right]
            if total == 0:
                return True
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return False

# Test cases
print(triples_sum_to_zero([1, 3, 5, 0]))  # False
print(triples_sum_to_zero([1, 3, -2, 1]))  # True
print(triples_sum_to_zero([1, 2, 3, 7]))  # False
print(triples_sum_to_zero([2, 4, -5, 3, 9, 7]))  # True
print(triples_sum_to_zero([1]))  # False