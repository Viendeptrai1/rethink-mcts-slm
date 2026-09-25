from typing import List

def sort_numbers(numbers: str) -> str:
    # Mapping of number words to their corresponding integer values
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
    
    # Split the input string into a list of words
    number_words = numbers.split()
    
    # Convert the list of words to a list of integers using the mapping
    number_values = [number_map[word] for word in number_words]
    
    # Sort the list of integers
    sorted_number_values = sorted(number_values)
    
    # Convert the sorted list of integers back to a list of words
    sorted_number_words = [list(number_map.keys())[value] for value in sorted_number_values]
    
    # Join the sorted list of words into a single string
    sorted_numbers_str = ' '.join(sorted_number_words)
    
    return sorted_numbers_str

# Example usage
print(sort_numbers('three one five'))  # Output: 'one three five'