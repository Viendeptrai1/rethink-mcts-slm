def search(lst):
    from collections import Counter
    
    freq = Counter(lst)
    max_value = -1
    
    for num in sorted(set(lst), reverse=True):
        if num > 0 and freq[num] >= num:
            return num
    
    return -1