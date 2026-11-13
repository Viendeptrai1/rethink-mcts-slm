from collections import Counter

def search(lst):
    freq = Counter(lst)
    for num in sorted(freq.keys(), reverse=True):
        if freq[num] >= num:
            return num
    return -1