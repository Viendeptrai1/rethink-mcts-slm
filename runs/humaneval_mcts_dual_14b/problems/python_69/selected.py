from collections import Counter

def search(lst):
    freq = Counter(lst)
    max_val = -1
    for num, count in freq.items():
        if count >= num:
            max_val = max(max_val, num)
    return max_val