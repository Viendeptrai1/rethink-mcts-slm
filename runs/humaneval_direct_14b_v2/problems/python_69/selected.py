def search(lst):
    from collections import Counter
    
    freq = Counter(lst)
    max_val = -1
    
    for num, count in freq.items():
        if num <= count and num > max_val:
            max_val = num
    
    return max_val