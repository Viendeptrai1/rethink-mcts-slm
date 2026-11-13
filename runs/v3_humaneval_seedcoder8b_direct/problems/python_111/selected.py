def histogram(test):
    if not test:
        return {}
    
    words = test.split()
    letter_counts = {}
    
    for word in words:
        for letter in word:
            letter_counts[letter] = letter_counts.get(letter, 0) + 1
    
    max_count = max(letter_counts.values())
    return {letter: count for letter, count in letter_counts.items() if count == max_count}