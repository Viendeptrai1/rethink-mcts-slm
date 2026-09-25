from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    # Step 1: Sort the list of numbers
    sorted_numbers = sorted(numbers)
    
    # Initialize variables to store the closest pair and the smallest difference found
    closest_pair = (sorted_numbers[0], sorted_numbers[1])
    smallest_diff = abs(sorted_numbers[1] - sorted_numbers[0])
    
    # Step 2: Iterate through the sorted list and find the closest pair
    for i in range(1, len(sorted_numbers) - 1):
        current_diff = abs(sorted_numbers[i + 1] - sorted_numbers[i])
        if current_diff < smallest_diff:
            smallest_diff = current_diff
            closest_pair = (sorted_numbers[i], sorted_numbers[i + 1])
    
    return closest_pair