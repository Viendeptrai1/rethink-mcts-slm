def histogram(test):
    if not test:
        return {}
    
    words = test.split()
    counts = {}
    
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    
    max_count = max(counts.values())
    result = {k: v for k, v in counts.items() if v == max_count}
    
    return result