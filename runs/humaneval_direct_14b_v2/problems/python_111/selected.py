def histogram(test):
    if not test:
        return {}
    
    # Split the input string into a list of letters
    letters = test.split()
    
    # Create a dictionary to count occurrences of each letter
    count_dict = {}
    for letter in letters:
        if letter in count_dict:
            count_dict[letter] += 1
        else:
            count_dict[letter] = 1
    
    # Find the maximum occurrence count
    max_count = max(count_dict.values())
    
    # Create a dictionary of letters with the maximum occurrence count
    result = {letter: count for letter, count in count_dict.items() if count == max_count}
    
    return result