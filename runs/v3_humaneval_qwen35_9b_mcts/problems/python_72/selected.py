def will_it_fly(q, w):
    if not q:
        return False
    
    total_sum = 0
    left = 0
    right = len(q) - 1
    
    while left <= right:
        if left != right:
            if q[left] != q[right]:
                return False
        total_sum += q[left]
        if left != right:
            total_sum += q[right]
        left += 1
        right -= 1
    
    return total_sum <= w