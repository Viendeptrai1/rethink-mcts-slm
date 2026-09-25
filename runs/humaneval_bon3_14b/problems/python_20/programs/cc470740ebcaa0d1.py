from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    if len(numbers) < 2:
        raise ValueError("The list must contain at least two numbers.")
    
    # Sort the numbers to make it easier to find the closest pair
    sorted_numbers = sorted(numbers)
    
    # Initialize variables to store the closest pair and the smallest difference found
    closest_pair = (sorted_numbers[0], sorted_numbers[1])
    smallest_diff = abs(sorted_numbers[1] - sorted_numbers[0])
    
    # Iterate through the sorted list and find the closest pair
    for i in range(1, len(sorted_numbers) - 1):
        diff = abs(sorted_numbers[i + 1] - sorted_numbers[i])
        if diff < smallest_diff:
            smallest_diff = diff
            closest_pair = (sorted_numbers[i], sorted_numbers[i + 1])
    
    return closest_pair