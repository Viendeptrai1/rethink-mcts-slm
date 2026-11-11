from typing import List

def sort_numbers(numbers: str) -> str:
    word_to_digit = {
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
    
    digit_to_word = {v: k for k, v in word_to_digit.items()}
    
    # Split the input string into words
    words = numbers.split()
    
    # Convert words to digits
    digits = [word_to_digit[word] for word in words]
    
    # Sort the digits
    sorted_digits = sorted(digits)
    
    # Convert sorted digits back to words
    sorted_words = [digit_to_word[digit] for digit in sorted_digits]
    
    # Join the sorted words into a single string
    return ' '.join(sorted_words)

# Example usage:
# result = sort_numbers('three one five')
# print(result)  # Output: 'one three five'