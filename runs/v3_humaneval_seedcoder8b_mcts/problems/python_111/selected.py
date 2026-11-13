def histogram(test):
    if not test:
        return {}
    
    letter_counts = {}
    for letter in test.split():
        letter_counts[letter] = letter_counts.get(letter, 0) + 1
    
    max_count = max(letter_counts.values())
    return {letter: count for letter, count in letter_counts.items() if count == max_count}