def histogram(test):
    if not test:
        return {}
    
    # Split the input string into a list of letters
    letters = test.split()
    
    # Create a dictionary to count occurrences of each letter
    counts = {}
    for letter in letters:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1
    
    # Find the maximum occurrence count
    max_count = max(counts.values())
    
    # Create a dictionary of letters with the maximum occurrence count
    result = {letter: count for letter, count in counts.items() if count == max_count}
    
    return result