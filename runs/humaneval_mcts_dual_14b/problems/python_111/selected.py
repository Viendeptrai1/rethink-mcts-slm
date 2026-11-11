def histogram(test):
    """Given a string representing a space separated lowercase letters, return a dictionary
    of the letter with the most repetition and containing the corresponding count.
    If several letters have the same occurrence, return all of them.
    """
    # Remove spaces and split the string into individual characters
    letters = test.replace(" ", "")
    
    # Dictionary to store the count of each letter
    count_dict = {}
    
    # Count occurrences of each letter
    for letter in letters:
        if letter in count_dict:
            count_dict[letter] += 1
        else:
            count_dict[letter] = 1
    
    # Find the maximum occurrence count
    if not count_dict:
        return {}
    
    max_count = max(count_dict.values())
    
    # Collect all letters with the maximum occurrence count
    result = {letter: count for letter, count in count_dict.items() if count == max_count}
    
    return result