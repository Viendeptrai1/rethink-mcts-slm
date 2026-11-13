def search(lst):
    from collections import Counter
    
    freq = Counter(lst)
    result = -1
    
    for num in sorted(set(lst), reverse=True):
        if num <= freq[num] and num > result:
            result = num
    
    return result