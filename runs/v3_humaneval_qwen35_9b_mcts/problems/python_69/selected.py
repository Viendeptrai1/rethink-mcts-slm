from collections import Counter

def search(lst):
    if not lst:
        return -1
    
    freq = Counter(lst)
    max_val = -1
    
    for num, count in freq.items():
        if num > 0 and count >= num:
            if count >= max_val:
                max_val = num
                
    return max_val