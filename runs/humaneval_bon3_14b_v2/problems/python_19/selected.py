from typing import List

def sort_numbers(numbers: str) -> str:
    num_dict = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }
    
    # Split the input string into a list of words
    words = numbers.split()
    
    # Sort the list of words based on their corresponding numeric values
    sorted_words = sorted(words, key=lambda word: num_dict[word])
    
    # Join the sorted list back into a string
    return ' '.join(sorted_words)