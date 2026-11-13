from collections import Counter

def search(lst):
    counts = Counter(lst)
    result = -1
    for num, freq in counts.items():
        if num > 0 and freq >= num:
            if freq >= result:
                result = num
    return result