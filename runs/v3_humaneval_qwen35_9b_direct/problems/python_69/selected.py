from collections import Counter

def search(lst):
    if not lst:
        return -1
    
    counts = Counter(lst)
    result = -1
    
    for num, freq in counts.items():
        if num > 0 and freq >= num:
            if freq >= result:
                result = num
    
    return result