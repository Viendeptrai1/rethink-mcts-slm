def histogram(test):
    """Given a string representing a space separated lowercase letters, return a dictionary
    of the letter with the most repetition and containing the corresponding count.
    If several letters have the same occurrence, return all of them.
    
    Example:
    histogram('a b c') == {'a': 1, 'b': 1, 'c': 1}
    histogram('a b b a') == {'a': 2, 'b': 2}
    histogram('a b c a b') == {'a': 2, 'b': 2}
    histogram('b b b b a') == {'b': 4}
    histogram('') == {}
    """
    if not test:
        return {}
    
    # Split the input string into individual letters, ignoring spaces
    letters = test.replace(" ", "")
    
    # Count the occurrences of each letter
    letter_counts = {}
    for letter in letters:
        if letter in letter_counts:
            letter_counts[letter] += 1
        else:
            letter_counts[letter] = 1
    
    # Find the maximum occurrence count
    max_count = max(letter_counts.values())
    
    # Create a dictionary of letters with the maximum occurrence count
    result = {letter: count for letter, count in letter_counts.items() if count == max_count}
    
    return result