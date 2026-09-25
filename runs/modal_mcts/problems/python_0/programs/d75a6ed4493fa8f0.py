from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    # Step 1: Sort the list of numbers
    sorted_numbers = sorted(numbers)
    
    # Step 2: Use a sliding window approach to check for close elements
    for i in range(len(sorted_numbers) - 1):
        if abs(sorted_numbers[i] - sorted_numbers[i + 1]) < threshold:
            return True
    
    return False