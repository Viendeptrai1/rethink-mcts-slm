from collections import Counter

def histogram(test):
    if not test:
        return {}
    
    # Split the string by spaces to get individual letters
    letters = test.split()
    
    # Count occurrences of each letter
    counter = Counter(letters)
    
    # Find the maximum count value
    max_count = max(counter.values())
    
    # Filter the counter to include only letters with the maximum count
    result = {letter: count for letter, count in counter.items() if count == max_count}
    
    return result