from typing import List

def sort_numbers(numbers: str) -> str:
    # Mapping of number words to their corresponding numeric values
    number_map = {
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
    
    # Split the input string into a list of number words
    number_words = numbers.split()
    
    # Sort the list of number words based on their numeric values
    sorted_number_words = sorted(number_words, key=lambda word: number_map[word])
    
    # Join the sorted list back into a space-delimited string
    sorted_numbers = ' '.join(sorted_number_words)
    
    return sorted_numbers

# Example usage
print(sort_numbers('three one five'))  # Output: 'one three five'