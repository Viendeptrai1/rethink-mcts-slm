from collections import Counter

def histogram(test):
    if not test:
        return {}
    
    letters = test.split()
    counts = Counter(letters)
    max_count = max(counts.values(), default=0)
    
    return {letter: count for letter, count in counts.items() if count == max_count}