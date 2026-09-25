from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    # Sort the list to reduce the number of comparisons
    sorted_numbers = sorted(numbers)
    
    # Iterate through the sorted list and check consecutive elements
    for i in range(len(sorted_numbers) - 1):
        if abs(sorted_numbers[i] - sorted_numbers[i + 1]) < threshold:
            return True
    
    return False