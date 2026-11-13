def triples_sum_to_zero(l: list):
    n = len(l)
    if n < 3:
        return False
    
    l.sort()
    
    for i in range(n - 2):
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = l[i] + l[left] + l[right]
            
            if current_sum == 0:
                return True
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return False